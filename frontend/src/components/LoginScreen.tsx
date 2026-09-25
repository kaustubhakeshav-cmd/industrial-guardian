import { useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { ShieldCheck, Lock, User } from 'lucide-react';

export function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, error, isLoading } = useAuthStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(username, password);
  };

  return (
    <div className="min-h-screen bg-industrial-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-industrial-900 border border-industrial-850 rounded-xl shadow-2xl p-8">
        <div className="flex flex-col items-center mb-8">
          <ShieldCheck className="w-16 h-16 text-alarm-info mb-4" />
          <h1 className="text-2xl font-bold text-industrial-heading">Industrial Guardian</h1>
          <p className="text-industrial-muted text-sm mt-1">Authorized Personnel Only</p>
        </div>

        {error && (
          <div className="mb-6 p-3 bg-alarm-critical/10 border border-alarm-critical/30 text-alarm-critical text-sm rounded text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-industrial-muted mb-1">Operator ID</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-industrial-muted" />
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-industrial-950 border border-industrial-850 text-industrial-heading rounded-md py-2.5 pl-10 pr-4 focus:outline-none focus:border-alarm-info focus:ring-1 focus:ring-alarm-info transition-colors"
                placeholder="e.g. operator"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-industrial-muted mb-1">Passcode</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-industrial-muted" />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-industrial-950 border border-industrial-850 text-industrial-heading rounded-md py-2.5 pl-10 pr-4 focus:outline-none focus:border-alarm-info focus:ring-1 focus:ring-alarm-info transition-colors"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-alarm-info hover:bg-blue-600 text-white font-medium py-2.5 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-4"
          >
            {isLoading ? 'Authenticating...' : 'Engage Dashboard'}
          </button>
        </form>
      </div>
    </div>
  );
}