import { useState } from 'react';
import { 
  Clock, 
  Car, 
  Wind,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Info
} from 'lucide-react';
import { CITY_METRICS } from '../data/puneData';

const AnalyticsPanel = () => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="absolute bottom-4 right-4 w-80 glass rounded-xl overflow-hidden">
      {/* Header */}
      <div 
        className="flex items-center justify-between p-4 cursor-pointer hover:bg-slate-700/30"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="text-white font-semibold">Demo Analytics</h3>
        {isExpanded ? <ChevronUp size={20} className="text-slate-400" /> : <ChevronDown size={20} className="text-slate-400" />}
      </div>

      {isExpanded && (
        <div className="p-4 pt-0 space-y-4">
          <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-3 text-xs text-amber-100">
            <strong>STATIC DEMO DATA</strong>
            <p className="mt-1 text-amber-100/80">These metrics are illustrative fixtures, not live measurements or verified government data.</p>
          </div>
          {/* KPI Cards */}
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <Clock size={14} className="text-slate-400" />
                <span className="text-slate-400 text-xs">Avg Travel Time</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold text-white">{CITY_METRICS.avgTravelTime}</span>
                <span className="text-slate-400 text-sm">min</span>
              </div>
            </div>

            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <Car size={14} className="text-slate-400" />
                <span className="text-slate-400 text-xs">Congestion</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold text-orange-400">{CITY_METRICS.congestionIndex}%</span>
              </div>
            </div>

            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <AlertTriangle size={14} className="text-slate-400" />
                <span className="text-slate-400 text-xs">Accidents/1K</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold text-white">{CITY_METRICS.accidentRate}</span>
              </div>
            </div>

            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <Wind size={14} className="text-slate-400" />
                <span className="text-slate-400 text-xs">Air Quality</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold text-red-400">{CITY_METRICS.airQualityIndex}</span>
                <span className="text-xs text-slate-500">AQI</span>
              </div>
            </div>
          </div>

          {/* Model availability */}
          <div className="rounded-lg border border-slate-600 bg-slate-800/70 p-4">
            <div className="flex items-center gap-2 text-white font-medium">
              <Info size={16} className="text-slate-300" />
              <span>Infrastructure analysis unavailable</span>
            </div>
            <p className="mt-2 text-xs leading-relaxed text-slate-400">
              No validated traffic feed, route-capacity dataset or evaluated ML model is connected. CityLens does not currently calculate a bridge-necessity score or predict project savings.
            </p>
          </div>

          {/* Scenario Impact Summary */}
          <div className="border-t border-slate-700 pt-3 text-center">
            <p className="text-xs text-slate-400">
              Scenario impact comparisons are not available until a calibrated traffic simulation is connected.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyticsPanel;
