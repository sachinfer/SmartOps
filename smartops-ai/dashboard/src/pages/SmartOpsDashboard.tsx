import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Gauge } from 'recharts';

export default function SmartOpsDashboard() {
  const [score, setScore] = useState<number | null>(null);
  const [statusMessage, setStatusMessage] = useState('Waiting for anomaly score...');
  const [restartStatus, setRestartStatus] = useState<string | null>(null);

  const fetchScore = async () => {
    try {
      const res = await fetch('/metrics');
      const text = await res.text();
      const match = text.match(/anomaly_score\s+([\d.]+)/);
      if (match) {
        const value = parseFloat(match[1]);
        setScore(value);
        if (value > 0.9) {
          setStatusMessage(`⚠️ High anomaly detected! Score = ${value}`);
        } else {
          setStatusMessage(`✅ Normal. Score = ${value}`);
        }
      } else {
        setStatusMessage('⚠️ anomaly_score not found.');
      }
    } catch (err) {
      setStatusMessage('Error fetching metrics.');
    }
  };

  const restartPod = async () => {
    try {
      const res = await fetch('/restart', { method: 'POST' });
      const json = await res.json();
      setRestartStatus(json.message);
    } catch (err) {
      setRestartStatus('Error restarting pod.');
    }
  };

  useEffect(() => {
    fetchScore();
    const interval = setInterval(fetchScore, 10000); // refresh every 10s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-1 gap-4 p-4 max-w-xl mx-auto">
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold mb-2">SmartOps Anomaly Score</h2>
          <div className="text-lg mb-4">{statusMessage}</div>
          <div className="mb-4">
            <Gauge
              width={300}
              height={200}
              domain={[0, 1]}
              value={score || 0}
              dataKey="value"
            />
          </div>
          <Button onClick={restartPod} className="w-full">
            🔁 Restart Anomaly Pod
          </Button>
          {restartStatus && <div className="mt-2 text-sm text-muted-foreground">{restartStatus}</div>}
        </CardContent>
      </Card>
    </div>
  );
} 