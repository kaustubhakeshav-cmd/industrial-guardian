import { create } from 'zustand';

interface SensorReading {
  sensor_id: string;
  subsystem: string;
  value: number;
  unit: string;
  status: 'NORMAL' | 'WARNING' | 'ANOMALY';
}

interface ChartPoint {
  time: string;
  pressure: number;
  flow: number;
  temp: number;
}

interface TelemetryState {
  connected: boolean;
  plantHealth: number;
  activeAnomalies: number;
  ttfHours: number | null; // <--- ADDED NEW STATE VARIABLE
  sensors: Record<string, SensorReading>;
  history: ChartPoint[];
  evidence: string[];
  connect: () => void;
}

export const useTelemetryStore = create<TelemetryState>((set, get) => ({
  connected: false,
  plantHealth: 100,
  activeAnomalies: 0,
  ttfHours: null, // <--- ADDED INITIAL STATE
  sensors: {},
  history: [],
  evidence: [],
  connect: () => {
    const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
    
    ws.onopen = () => {
      set({ connected: true });
    };
    
    ws.onclose = () => {
      set({ connected: false });
      setTimeout(() => get().connect(), 5000);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const timeString = new Date(data.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        set((state) => {
          const newHistory = [...state.history, {
            time: timeString,
            pressure: data.sensors.PUMP_PRESSURE?.value || 0,
            flow: data.sensors.FLOW_RATE?.value || 0,
            temp: data.sensors.REACTOR_TEMP?.value || 0
          }].slice(-60);

          return {
            plantHealth: data.plant_health,
            activeAnomalies: data.active_anomalies,
            ttfHours: data.estimated_ttf_hours, // <--- MAPPED INCOMING DATA
            sensors: data.sensors,
            history: newHistory,
            evidence: data.evidence || []
          };
        });
      } catch (error) {
        console.error("Failed to parse telemetry frame", error);
      }
    };
  }
}));