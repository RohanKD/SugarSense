import { useState } from 'react';
import './globals.css';

export default function AnalyzeBloodData() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    } else {
      alert('Please upload a PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a PDF file first.");
      return;
    }

    const formData = new FormData();
formData.append('file', file);

    try {
    const response = await fetch('http://localhost:5000/analyze-pdf', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const data = await response.json();
        setAnalysis(data.analysis);
    } else {
        const errorText = await response.text(); 
        console.error("Server responded with an error:", errorText);
        alert("Failed to analyze PDF: " + errorText);
    }
    } catch (error) {
    console.error("Network or fetch error:", error);  
    alert("Network error or failed to analyze PDF");
    } finally {
    setLoading(false);
    }

  };

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Blood Data Analysis</h1>

        {/* Upload PDF File */}
        <div className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4">Upload Blood Data PDF</h2>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
            style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }}
          />
          <button
            onClick={handleUpload}
            className="w-full mt-4 px-4 py-2 font-semibold rounded-md"
            style={{ backgroundColor: '#16384F', color: '#FCEDE9' }}
          >
            {loading ? "Processing..." : "Upload and Analyze PDF"}
          </button>
        </div>

        {/* Display Analysis Results */}
        {analysis && (
          <div className="p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
            <h2 className="text-2xl font-semibold mb-4">Analysis Results</h2>
            <p className="text-lg" style={{ color: '#2D799C' }}>
              <strong>Summary Insights:</strong>
            </p>
            <p>{analysis.match(/<summary_insights>(.*?)<\/summary_insights>/s)?.[1]}</p>
            <p className="text-lg mt-4" style={{ color: '#2D799C' }}>
              <strong>Recommendations:</strong>
            </p>
            <p>{analysis.match(/<recommendations>(.*?)<\/recommendations>/s)?.[1]}</p>
          </div>
        )}
      </div>
    </div>
  );
}
