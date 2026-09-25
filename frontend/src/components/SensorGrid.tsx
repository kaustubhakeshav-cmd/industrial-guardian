import { useTelemetryStore } from '../store/useTelemetryStore';
import { AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

export function SensorGrid() {
  const sensors = useTelemetryStore((state) => state.sensors);
  const sensorList = Object.values(sensors);

  if (sensorList.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-industrial-muted border border-dashed border-industrial-850 rounded-lg p-6">
        Waiting for sensor telemetry...
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
      {sensorList.map((sensor) => {
        // Determine styles based on sensor status
        let cardStyle = 'bg-industrial-900 border-industrial-850';
        let textStyle = 'text-industrial-heading';
        let Icon = CheckCircle2;
        let iconColor = 'text-alarm-nominal';

        if (sensor.status === 'ANOMALY') {
          cardStyle = 'bg-alarm-critical/10 border-alarm-critical/50 shadow-[0_0_15px_rgba(239,68,68,0.1)]';
          textStyle = 'text-alarm-critical';
          Icon = AlertCircle;
          iconColor = 'text-alarm-critical';
        } else if (sensor.status === 'WARNING') {
          cardStyle = 'bg-alarm-warning/10 border-alarm-warning/50';
          textStyle = 'text-alarm-warning';
          Icon = AlertTriangle;
          iconColor = 'text-alarm-warning';
        }

        return (
          <div key={sensor.sensor_id} className={`border rounded-md p-3 flex flex-col justify-between transition-colors duration-300 ${cardStyle}`}>
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-mono text-industrial-muted truncate pr-2" title={sensor.sensor_id}>
                {sensor.sensor_id.replace(/_/g, ' ')}
              </span>
              <Icon className={`w-4 h-4 flex-shrink-0 ${iconColor}`} />
            </div>
            
            <div>
              <div className="text-[10px] text-industrial-muted mb-0.5">{sensor.subsystem}</div>
              <div className="flex items-baseline gap-1">
                <span className={`text-lg font-bold font-mono ${textStyle}`}>
                  {sensor.value.toFixed(2)}
                </span>
                <span className="text-xs text-industrial-muted">{sensor.unit}</span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}