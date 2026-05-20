import { useEffect, useState } from 'react';
import { Closure } from './types';

const App = () => {
  const [closures, setClosures] = useState<Closure[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClosures = async () => {
      try {
        const response = await fetch('http://localhost:8000/closures');
        if (!response.ok) {
          throw new Error('Failed to fetch closure data');
        }
        const data = await response.json();
        setClosures(data);
      } catch (err) {
        console.error('Fetch error:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchClosures();
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading closures...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>Error: {error}</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Restaurant Closures (Last 6 Months)</h1>
      {closures.length === 0 ? (
        <p>No closures found.</p>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr style={{ textAlign: 'left', borderBottom: '2px solid #ccc' }}>
              <th style={{ padding: '10px' }}>Establishment</th>
              <th style={{ padding: '10px' }}>Address</th>
              <th style={{ padding: '10px' }}>Closed On</th>
              <th style={{ padding: '10px' }}>Reopened On</th>
              <th style={{ padding: '10px' }}>Reason</th>
            </tr>
          </thead>
          <tbody>
            {closures.map((closure) => (
              <tr key={closure.uuid} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '10px' }}>
                  <strong>{closure.establishment.name}</strong>
                  {closure.establishment.permit_name && (
                    <div style={{ fontSize: '0.8em', color: '#666' }}>
                      DBA: {closure.establishment.permit_name}
                    </div>
                  )}
                </td>
                <td style={{ padding: '10px' }}>
                  {closure.establishment.address}<br/>
                  <span style={{ fontSize: '0.9em', color: '#555' }}>
                    {closure.establishment.city}, {closure.establishment.zip}
                  </span>
                </td>
                <td style={{ padding: '10px' }}>
                  {closure.closed_on ? new Date(closure.closed_on).toLocaleDateString() : 'N/A'}
                </td>
                <td style={{ padding: '10px' }}>
                  {closure.reopened_on 
                    ? new Date(closure.reopened_on).toLocaleDateString() 
                    : <span style={{ color: '#d9534f', fontWeight: 'bold' }}>Still Closed</span>}
                </td>
                <td style={{ padding: '10px' }}>{closure.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      )}
    </div>
  );
};

export default App;