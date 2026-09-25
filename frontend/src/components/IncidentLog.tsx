import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { Database, X, AlertOctagon, Clock } from 'lucide-react';

interface Incident {
  id: number;
  timestamp: string;
  plant_health: number;
  ai_evidence: string[];
}

export function IncidentLog() {
  const [isOpen, setIsOpen] = useState(false);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(false);
  const { token } = useAuthStore();

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/history/anomalies', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setIncidents(data);
      }
    } catch (error) {
      console.error("Failed to fetch incident history", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 bg-industrial-900 border border-industrial-850 hover:bg-industrial-800 px-4 py-2 rounded-md transition-colors text-industrial-muted hover:text-industrial-heading"
      >
        <Database className="w-4 h-4" />
        <span>Audit Log</span>
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-industrial-950 border border-industrial-850 rounded-xl w-full max-w-4xl max-h-[80vh] flex flex-col shadow-2xl">
            <div className="flex items-center justify-between p-4 border-b border-industrial-850">
              <h2 className="text-xl font-bold text-industrial-heading flex items-center gap-2">
                <Database className="w-5 h-5 text-alarm-info" />
                Historical Incident Review
              </h2>
              <button onClick={() => setIsOpen(false)} className="text-industrial-muted hover:text-white">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-4 overflow-y-auto flex-grow flex flex-col gap-3">
              {loading ? (
                <div className="text-center text-industrial-muted py-8">Querying database...</div>
              ) : incidents.length === 0 ? (
                <div className="text-center text-industrial-muted py-8">No historical anomalies recorded.</div>
              ) : (
                incidents.map((incident) => (
                  <div key={incident.id} className="bg-industrial-900 border border-industrial-850 rounded p-4 flex gap-4">
                    <div className="flex-shrink-0 mt-1">
                      <AlertOctagon className="w-6 h-6 text-alarm-critical" />
                    </div>
                    <div className="flex-grow">
                      <div className="flex items-center gap-4 mb-2">
                        <span className="text-sm font-mono text-industrial-muted flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {new Date(incident.timestamp).toLocaleString()}
                        </span>
                        <span className="text-xs font-mono bg-alarm-critical/20 text-alarm-critical px-2 py-0.5 rounded border border-alarm-critical/30">
                          ID: {incident.id}
                        </span>
                        <span className="text-sm font-mono text-alarm-warning">
                          Health Drop: {incident.plant_health.toFixed(1)}%
                        </span>
                      </div>
                      <div className="space-y-1 text-sm text-industrial-text">
                        {incident.ai_evidence.map((ev, idx) => (
                          <div key={idx} className="bg-industrial-950 px-3 py-1.5 rounded border border-industrial-850 font-mono text-xs">
                            {ev}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}