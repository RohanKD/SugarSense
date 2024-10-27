import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import './globals.css';

export default function SugarDashboard() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState('');
  const [sugarLevels, setSugarLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newReading, setNewReading] = useState('');
  const [readingTime, setReadingTime] = useState('');

  useEffect(() => {
    const fetchSugarLevels = async () => {
      try {
        const response = await fetch('/api/sugar-levels');
        if (!response.ok) {
          throw new Error('Failed to fetch sugar levels');
        }
        const data = await response.json();
        setSugarLevels(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching sugar levels:', error);
        setLoading(false);
      }
    };
    fetchSugarLevels();
  }, []);

  const handleAddReading = async () => {
    if (!newReading || !readingTime) return;

    try {
      const response = await fetch('/api/sugar-levels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level: newReading, time: readingTime }),
      });
      if (response.ok) {
        const updatedData = await response.json();
        setSugarLevels(updatedData);
        setNewReading('');
        setReadingTime('');
      } else {
        console.error('Failed to add sugar level');
      }
    } catch (error) {
      console.error('Error adding sugar level:', error);
    }
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredSugarLevels = sugarLevels.filter((reading) =>
    reading.time.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="min-h-screen" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>Loading...</div>;
  }

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Blood Sugar Dashboard</h1>

        {/* Search Input */}
        <div className="mb-8">
          <input
            type="text"
            value={searchTerm}
            onChange={handleSearch}
            placeholder="Search by date..."
            className="w-full px-4 py-2 rounded-md border border-gray-300 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
            style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }}
          />
        </div>

        {/* Add New Reading */}
        <div className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4">Add New Reading</h2>
          <div className="flex flex-col space-y-4">
            <input
              type="number"
              value={newReading}
              onChange={(e) => setNewReading(e.target.value)}
              placeholder="Enter blood sugar level (mg/dL)"
              className="w-full px-4 py-2 rounded-md border border-gray-300 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
              style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }}
            />
            <input
              type="datetime-local"
              value={readingTime}
              onChange={(e) => setReadingTime(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
              style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }}
            />
            <button
              onClick={handleAddReading}
              className="w-full px-4 py-2 font-semibold rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
              style={{ backgroundColor: '#16384F', color: '#FCEDE9' }}
            >
              Add Reading
            </button>
          </div>
        </div>

        {/* Blood Sugar History */}
        <div className="p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4">Blood Sugar History</h2>
          <ul className="divide-y divide-gray-300">
            {filteredSugarLevels.map((reading) => (
              <li key={reading.id} className="py-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-medium" style={{ color: '#2D799C' }}>Level: {reading.level} mg/dL</h3>
                    <p className="mt-1 text-sm text-gray-500">
                      Time: {new Date(reading.time).toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <button
                      onClick={() => console.log("Viewing details for reading ID:", reading.id)}
                      className="px-3 py-1 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300"
                      style={{ backgroundColor: '#16384F', color: '#FCEDE9' }}
                    >
                      View Details
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
