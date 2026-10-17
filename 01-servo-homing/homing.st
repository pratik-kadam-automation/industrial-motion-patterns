(* NOTE: written vendor-neutral and not compiled against a specific toolchain.
   Syntax-check in your PLC IDE and map I/O to your own motion instructions. *)

(* 4-step axis homing as a state machine - IEC 61131-3 Structured Text.
   Vendor-neutral: map the inputs/outputs to your PLC's own motion instructions.
   Limit switches are handled HERE in logic, so the axis protects itself
   even if the drive configuration is wrong. *)

TYPE HomingState : (IDLE, FAST_SEARCH, BACK_OFF, CREEP, ZERO_SET, DONE, FAULT); END_TYPE

FUNCTION_BLOCK FB_Homing
VAR_INPUT
    Start       : BOOL;      (* rising edge starts homing *)
    HomeSensor  : BOOL;      (* TRUE when carriage is on the sensor *)
    LimitNeg    : BOOL;      (* hardware limit, TRUE = tripped *)
    LimitPos    : BOOL;
    Position    : REAL;      (* current axis position, mm *)
    Abort       : BOOL;
END_VAR
VAR_OUTPUT
    CmdVelocity : REAL;      (* mm/s, signed. Send to your drive/motion block *)
    ZeroNow     : BOOL;      (* one-scan pulse: set current position as origin *)
    Done        : BOOL;
    State       : HomingState;
END_VAR
VAR_INPUT
    V_FAST      : REAL := 200.0;
    V_CREEP     : REAL := 5.0;
    BACKOFF_MM  : REAL := 10.0;
    TIMEOUT     : TIME := T#30s;
END_VAR
VAR
    startPos    : REAL;
    tmo         : TON;
    rStart      : R_TRIG;
END_VAR

rStart(CLK := Start);
tmo(IN := (State <> IDLE) AND (State <> DONE) AND (State <> FAULT), PT := TIMEOUT);
ZeroNow := FALSE;

(* Safety first: any limit, abort, or timeout drops to FAULT with zero velocity *)
IF Abort OR tmo.Q OR (LimitPos AND CmdVelocity > 0.0) OR (LimitNeg AND CmdVelocity < 0.0) THEN
    State := FAULT;
END_IF;

CASE State OF
    IDLE:
        CmdVelocity := 0.0; Done := FALSE;
        IF rStart.Q THEN State := FAST_SEARCH; END_IF;

    FAST_SEARCH:                         (* 1. quick approach, saves cycle time *)
        CmdVelocity := -V_FAST;
        IF HomeSensor THEN
            startPos := Position; State := BACK_OFF;
        END_IF;

    BACK_OFF:                            (* 2. retreat past the sensor edge *)
        CmdVelocity := V_FAST;
        IF (NOT HomeSensor) AND (ABS(Position - startPos) >= BACKOFF_MM) THEN
            State := CREEP;
        END_IF;

    CREEP:                               (* 3. slow re-approach: repeatable trigger point *)
        CmdVelocity := -V_CREEP;
        IF HomeSensor THEN
            CmdVelocity := 0.0; State := ZERO_SET;
        END_IF;

    ZERO_SET:                            (* 4. latch origin *)
        ZeroNow := TRUE; State := DONE;

    DONE:
        CmdVelocity := 0.0; Done := TRUE;
        IF NOT Start THEN State := IDLE; END_IF;

    FAULT:
        CmdVelocity := 0.0; Done := FALSE;
        IF NOT Start AND NOT Abort THEN State := IDLE; END_IF;
END_CASE;
END_FUNCTION_BLOCK
