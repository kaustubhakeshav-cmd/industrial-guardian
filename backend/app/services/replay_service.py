import math
import random
from datetime import datetime, timezone
from app.data.schemas import TelemetryFrame, SensorReading, AnomalyEvidence, SensorContribution
from app.core.config import settings

class TelemetryReplayEngine:
    def __init__(self):
        self.tick = 0
        self.is_anomaly_mode = False
        self.anomaly_duration = 0

    def get_next_frame(self) -> TelemetryFrame:
        self.tick += 1
        now = datetime.now(timezone.utc)
        
        # Inject periodic anomaly cycles for real-time testing
        if self.tick % 40 == 0:
            self.is_anomaly_mode = True
            self.anomaly_duration = 12

        if self.anomaly_duration > 0:
            self.anomaly_duration -= 1
        else:
            self.is_anomaly_mode = False

        # Simulate core process variables
        base_noise = lambda: random.uniform(-0.5, 0.5)
        
        # Sensor simulations
        p_val = 72.4 + math.sin(self.tick * 0.1) * 2.0 + (18.5 if self.is_anomaly_mode else 0.0) + base_noise()
        t_val = 145.2 + math.cos(self.tick * 0.08) * 1.5 + (12.3 if self.is_anomaly_mode else 0.0) + base_noise()
        f_val = 38.7 + math.sin(self.tick * 0.05) * 1.2 - (15.2 if self.is_anomaly_mode else 0.0) + base_noise()
        v_val = 2.3 + math.cos(self.tick * 0.12) * 0.2 + (1.9 if self.is_anomaly_mode else 0.0) + base_noise()
        ph_val = 7.1 + math.sin(self.tick * 0.02) * 0.05 + base_noise() * 0.02
        mw_val = 5.8 + math.cos(self.tick * 0.04) * 0.1 + (0.8 if self.is_anomaly_mode else 0.0) + base_noise() * 0.05

        score = 0.88 if self.is_anomaly_mode else max(0.12, min(0.35, 0.22 + math.sin(self.tick * 0.2) * 0.08))
        status_label = "CRITICAL" if score >= settings.CRITICAL_ANOMALY_THRESHOLD else ("WARNING" if score >= settings.DEFAULT_ANOMALY_THRESHOLD else "NOMINAL")

        evidence = None
        if score >= settings.DEFAULT_ANOMALY_THRESHOLD:
            evidence = AnomalyEvidence(
                anomaly_score=round(score, 3),
                threshold=settings.DEFAULT_ANOMALY_THRESHOLD,
                status=status_label,
                timestamp=now,
                alarm_triggered=True,
                affected_sensors=[
                    SensorContribution(
                        sensor_id="FLOW_RATE_01",
                        subsystem="Heat Exchanger",
                        contribution=0.92,
                        current_value=round(f_val, 2),
                        baseline_value=38.7,
                        unit="m³/h"
                    ),
                    SensorContribution(
                        sensor_id="PUMP_PRESSURE_01",
                        subsystem="Pump B",
                        contribution=0.87,
                        current_value=round(p_val, 2),
                        baseline_value=72.4,
                        unit="bar"
                    ),
                    SensorContribution(
                        sensor_id="REACTOR_TEMP_01",
                        subsystem="Reactor A",
                        contribution=0.64,
                        current_value=round(t_val, 2),
                        baseline_value=145.2,
                        unit="°C"
                    ),
                    SensorContribution(
                        sensor_id="TURBINE_VIB_01",
                        subsystem="Turbine",
                        contribution=0.42,
                        current_value=round(v_val, 2),
                        baseline_value=2.3,
                        unit="mm/s"
                    )
                ]
            )

        sensors = {
            "PUMP_PRESSURE": SensorReading(
                sensor_id="PUMP_PRESSURE",
                subsystem="Pump B",
                value=round(p_val, 2),
                unit="bar",
                status="ANOMALY" if self.is_anomaly_mode else "NORMAL"
            ),
            "REACTOR_TEMP": SensorReading(
                sensor_id="REACTOR_TEMP",
                subsystem="Reactor A",
                value=round(t_val, 2),
                unit="°C",
                status="WARNING" if self.is_anomaly_mode else "NORMAL"
            ),
            "FLOW_RATE": SensorReading(
                sensor_id="FLOW_RATE",
                subsystem="Heat Exchanger",
                value=round(f_val, 2),
                unit="m³/h",
                status="ANOMALY" if self.is_anomaly_mode else "NORMAL"
            ),
            "TURBINE_VIBRATION": SensorReading(
                sensor_id="TURBINE_VIBRATION",
                subsystem="Turbine",
                value=round(v_val, 2),
                unit="mm/s",
                status="WARNING" if self.is_anomaly_mode else "NORMAL"
            ),
            "PH_LEVEL": SensorReading(
                sensor_id="PH_LEVEL",
                subsystem="Water Treatment",
                value=round(ph_val, 2),
                unit="pH",
                status="NORMAL"
            ),
            "POWER_CONSUMPTION": SensorReading(
                sensor_id="POWER_CONSUMPTION",
                subsystem="Compressor",
                value=round(mw_val, 2),
                unit="MW",
                status="NORMAL"
            )
        }

        return TelemetryFrame(
            timestamp=now,
            plant_health=82.4 if self.is_anomaly_mode else 98.7,
            active_anomalies=3 if self.is_anomaly_mode else 0,
            open_incidents=2 if self.is_anomaly_mode else 0,
            sensors=sensors,
            evidence=evidence
        )

replay_engine = TelemetryReplayEngine()