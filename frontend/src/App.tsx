import { useEffect } from 'react';
import { useTelemetryStore } from './store/useTelemetryStore';
import { useAuthStore } from './store/useAuthStore';
import { ShieldCheck, AlertTriangle, Activity, BrainCircuit, LogOut, Timer } from 'lucide-react';
import { LiveTelemetryChart } from './components/LiveTelemetryChart';
import { SensorGrid } from './components/SensorGrid';
import { LoginScreen } from './components/LoginScreen';
import { IncidentLog } from './components/IncidentLog';

// Helper function to decode the JWT payload natively in the browser
const getRoleFromToken = (token: string | null): string => {
  if (!token) return 'Operator';
  try {
    const payloadBase64 = token.split('.')[1];
    const decodedJson = atob(payloadBase64);
    const payload = JSON.parse(decodedJson);
    return payload.role || 'Operator';
  } catch (error) {
    console.error("Failed to parse token role", error);
    return 'Operator';
  }
};

export default function App() {
  // Destructure ttfHours from the store
  const { connected, plantHealth, activeAnomalies, ttfHours, evidence, connect } = useTelemetryStore();
  const { token, logout } = useAuthStore();

  useEffect(() => {
    if (token) {
      connect();
    }
  }, [connect, token]);

  // Protect the route
  if (!token) {
    return <LoginScreen />;
  }

  // Extract the user's role directly from their active session token
  const userRole = getRoleFromToken(token);

  return (
    <div className="min-h-screen bg-industrial-950 text-industrial-text p-4 flex flex-col gap-6">
      <header className="flex items-center justify-between border-b border-industrial-850 pb-4">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-8 h-8 text-alarm-info" />
          <div>
            <h1 className="text-industrial-heading font-bold text-xl leading-none">Industrial Guardian</h1>
            <span className="text-xs text-industrial-muted">AI-Powered Anomaly Detection</span>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-sm font-mono">
          <div className="border border-industrial-850 bg-industrial-900 px-4 py-2 rounded-md shadow-sm flex items-center gap-2">
            <div className={`w-2.5 h-2.5 rounded-full ${connected ? 'bg-alarm-nominal animate-pulse' : 'bg-alarm-critical'}`} />
            <span>{connected ? 'WS: CONNECTED' : 'WS: DISCONNECTED'}</span>
          </div>
          
          {/* Only render the Historical Incident Modal if the user has Investigator clearance */}
          {userRole === 'Investigator' && <IncidentLog />}
          
          <button 
            onClick={logout}
            className="flex items-center gap-2 bg-industrial-900 border border-industrial-850 hover:bg-industrial-800 px-4 py-2 rounded-md transition-colors text-industrial-muted hover:text-industrial-heading"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </header>

      {/* Main KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-industrial-900 border border-industrial-850 p-4 rounded-lg flex items-center justify-between shadow-sm">
          <div>
            <p className="text-industrial-muted text-sm mb-1">System Health</p>
            <p className={`text-2xl font-mono font-bold transition-colors ${plantHealth < 100 ? 'text-alarm-warning' : 'text-industrial-heading'}`}>
              {plantHealth.toFixed(1)}%
            </p>
          </div>
          <Activity className={`w-8 h-8 opacity-80 ${plantHealth < 100 ? 'text-alarm-warning' : 'text-alarm-nominal'}`} />
        </div>

        <div className="bg-industrial-900 border border-industrial-850 p-4 rounded-lg flex items-center justify-between shadow-sm">
          <div>
            <p className="text-industrial-muted text-sm mb-1">Active Anomalies</p>
            <p className={`text-2xl font-mono font-bold transition-colors ${activeAnomalies > 0 ? 'text-alarm-critical' : 'text-industrial-heading'}`}>
              {activeAnomalies}
            </p>
          </div>
          <AlertTriangle className={`w-8 h-8 transition-colors ${activeAnomalies > 0 ? 'text-alarm-critical' : 'text-industrial-muted'} opacity-80`} />
        </div>

        {/* New Predictive Maintenance Card */}
        <div className="bg-industrial-900 border border-industrial-850 p-4 rounded-lg flex items-center justify-between shadow-sm">
          <div>
            <p className="text-industrial-muted text-sm mb-1">Predicted Time-To-Failure</p>
            {ttfHours !== null ? (
              <p className="text-2xl font-mono font-bold text-alarm-critical animate-pulse">
                {ttfHours.toFixed(1)} <span className="text-sm text-industrial-muted font-sans">hrs</span>
              </p>
            ) : (
              <p className="text-2xl font-mono font-bold text-industrial-muted">
                Nominal
              </p>
            )}
          </div>
          <Timer className={`w-8 h-8 opacity-80 ${ttfHours !== null ? 'text-alarm-critical' : 'text-industrial-muted'}`} />
        </div>
      </div>
      
      {/* Main Content Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 bg-industrial-900 border border-industrial-850 p-4 rounded-lg flex flex-col shadow-sm min-h-[400px]">
          <h2 className="text-industrial-heading font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-industrial-muted" />
            Live Process Overview
          </h2>
          <div className="flex-grow">
            <LiveTelemetryChart />
          </div>
        </div>

        <div className="bg-industrial-900 border border-industrial-850 p-4 rounded-lg shadow-sm flex flex-col h-[400px]">
          <h2 className="text-industrial-heading font-semibold mb-4 flex items-center gap-2">
            <BrainCircuit className="w-4 h-4 text-alarm-info" />
            System Intelligence
          </h2>
          <div className="flex-grow flex flex-col gap-3 overflow-y-auto pr-2">
            {evidence.length === 0 ? (
              <div className="flex-grow flex items-center justify-center text-industrial-muted border border-dashed border-industrial-850 rounded p-4 text-sm text-center">
                System operating within normal parameters. Transformer network monitoring active.
              </div>
            ) : (
              evidence.map((msg, idx) => (
                <div key={idx} className="bg-alarm-critical/10 border border-alarm-critical/30 rounded p-3 text-sm text-alarm-critical flex items-start gap-2 shadow-[0_0_10px_rgba(239,68,68,0.05)]">
                  <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <div>
                    <span className="font-bold block mb-1">AI DETECTED ANOMALY</span>
                    {msg}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="bg-industrial-900 border border-industrial-850 p-4 rounded-lg shadow-sm">
        <h2 className="text-industrial-heading font-semibold mb-4 flex items-center gap-2">
          <Activity className="w-4 h-4 text-industrial-muted" />
          Subsystem Sensor Matrix
        </h2>
        <SensorGrid />
      </div>
    </div>
  );
}