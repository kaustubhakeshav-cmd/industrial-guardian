import ReactECharts from 'echarts-for-react';
import { useTelemetryStore } from '../store/useTelemetryStore';

export function LiveTelemetryChart() {
  const history = useTelemetryStore((state) => state.history);

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#101826',
      borderColor: '#23344D',
      textStyle: { color: '#F8FAFC' }
    },
    legend: {
      data: ['Pump Pressure (bar)', 'Flow Rate (m³/h)', 'Reactor Temp (°C)'],
      textStyle: { color: '#94A3B8' },
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: history.map(item => item.time),
      axisLine: { lineStyle: { color: '#23344D' } },
      axisLabel: { color: '#64748B' }
    },
    yAxis: [
      {
        type: 'value',
        name: 'Pressure/Flow',
        nameTextStyle: { color: '#64748B' },
        splitLine: { lineStyle: { color: '#162234' } },
        axisLabel: { color: '#94A3B8' }
      },
      {
        type: 'value',
        name: 'Temp (°C)',
        nameTextStyle: { color: '#64748B' },
        splitLine: { show: false },
        axisLabel: { color: '#94A3B8' }
      }
    ],
    series: [
      {
        name: 'Pump Pressure (bar)',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2, color: '#3B82F6' },
        data: history.map(item => item.pressure)
      },
      {
        name: 'Flow Rate (m³/h)',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 2, color: '#10B981' },
        data: history.map(item => item.flow)
      },
      {
        name: 'Reactor Temp (°C)',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        showSymbol: false,
        lineStyle: { width: 2, color: '#F59E0B' },
        data: history.map(item => item.temp)
      }
    ],
    animation: false // Disable default animation for high-frequency live data
  };

  return (
    <div className="w-full h-full min-h-[350px]">
      <ReactECharts 
        option={option} 
        style={{ height: '100%', width: '100%' }} 
        opts={{ renderer: 'canvas' }} 
      />
    </div>
  );
}