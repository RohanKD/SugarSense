import { useState } from 'react';
import './globals.css';

export default function UploadData() {
  // States for various form inputs
  const [foodItem, setFoodItem] = useState('');
  const [calories, setCalories] = useState('');
  const [carbs, setCarbs] = useState('');
  const [foodTime, setFoodTime] = useState('');

  const [medName, setMedName] = useState('');
  const [dosage, setDosage] = useState('');
  const [medTime, setMedTime] = useState('');

  const [activityType, setActivityType] = useState('');
  const [duration, setDuration] = useState('');
  const [intensity, setIntensity] = useState('');

  // States for CSV, ECG, and button appearance
  const [file, setFile] = useState(null);
  const [ecgFile, setEcgFile] = useState(null);
  const [graphImage, setGraphImage] = useState(null);
  const [ecgGraphImage, setEcgGraphImage] = useState(null);
  const [eyeFundusImage, setEyeFundusImage] = useState(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);

  

  // Button states to track if a file has been uploaded
  const [foodButtonPressed, setFoodButtonPressed] = useState(false);
  const [medButtonPressed, setMedButtonPressed] = useState(false);
  const [activityButtonPressed, setActivityButtonPressed] = useState(false);
  const [csvButtonPressed, setCsvButtonPressed] = useState(false);
  const [ecgButtonPressed, setEcgButtonPressed] = useState(false);
  const [eyeFundusButtonPressed, setEyeFundusButtonPressed] = useState(false);
  const [showReport, setShowReport] = useState(false);

// Submit handlers for each section with field clearing
const handleSubmitFood = (e) => {
    e.preventDefault();
    setFoodButtonPressed(true);
    // Reset food intake fields
    setFoodItem('');
    setCalories('');
    setCarbs('');
    setFoodTime('');
  };
  
  const handleSubmitMed = (e) => {
    e.preventDefault();
    setMedButtonPressed(true);
    // Reset medication fields
    setMedName('');
    setDosage('');
    setMedTime('');
  };
  
  const handleSubmitActivity = (e) => {
    e.preventDefault();
    setActivityButtonPressed(true);
    // Reset activity fields
    setActivityType('');
    setDuration('');
    setIntensity('');
  };

  // Handle file changes and keep button status
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setCsvButtonPressed(true);
    } else {
      alert('Please upload a CSV file.');
    }
  };

  const handleEcgFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setEcgFile(selectedFile);
      setEcgButtonPressed(true);
    } else {
      alert('Please upload a CSV file.');
    }
  };
  const handleEyeFundusFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'image/png') setEyeFundusFile(selectedFile);
    else alert('Please upload a PNG file.');
  };
  const handleProcessCSV = async () => {
    if (!file) {
      alert("Please upload a CSV file first.");
      return;
    }
    if (!startDate || !endDate) {
      alert("Please select both a start and end date.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('start_date', startDate);
    formData.append('end_date', endDate);

    try {
      const response = await fetch('http://localhost:5000/upload-csv', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const imageBlob = await response.blob();
        const imageURL = URL.createObjectURL(imageBlob);
        setGraphImage(imageURL);
      } else {
        alert("Failed to process CSV");
      }
    } catch (error) {
      console.error("Error processing CSV:", error);
      alert("Error processing CSV");
    }
  };

  const handleAnalyzeECG = async () => {
    /*
    if (!ecgFile) {
      alert("Please upload an ECG CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', ecgFile);

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/analyze-ecg', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const imageBlob = await response.blob();
        const imageURL = URL.createObjectURL(imageBlob);
        setEcgGraphImage(imageURL);
      } else {
        alert("Failed to analyze ECG data");
      }
    } catch (error) {
      console.error("Error analyzing ECG:", error);
      alert("Error analyzing ECG");
    } finally {
      setLoading(false);
    }
    */
  };
  const handleUploadEyeFundus = async () => {
    /*
    if (!eyeFundusFile) {
      alert("Please upload an Eye Fundus PNG file first.");
      return;
    }
    const formData = new FormData();
    formData.append('file', eyeFundusFile);

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/analyze-eye-fundus', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const imageBlob = await response.blob();
        setEyeFundusImage(URL.createObjectURL(imageBlob));
        setEyeFundusButtonPressed(true);
      } else alert("Failed to upload Eye Fundus Image");
    } catch (error) {
      console.error("Error uploading Eye Fundus Image:", error);
      alert("Error uploading Eye Fundus Image");
    } finally {
      setLoading(false);
    }
      */
  };
  const handleToggleReport = () => {
    setShowReport(!showReport);
  };
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6" style={{ color: '#2D799C' }}>Upload Data</h1>

        {/* Food Intake Entry */}
        <form onSubmit={handleSubmitFood} className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Food Intake Entry</h2>
          <div className="flex flex-col space-y-4">
            <input type="text" placeholder="Food Item" value={foodItem} onChange={(e) => setFoodItem(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="number" placeholder="Calories" value={calories} onChange={(e) => setCalories(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="number" placeholder="Carbohydrates (g)" value={carbs} onChange={(e) => setCarbs(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="datetime-local" value={foodTime} onChange={(e) => setFoodTime(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
          </div>
          <button type="submit" className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${foodButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`}
            style={{ color: '#FCEDE9' }}>
            {foodButtonPressed ? "Reupload File" : "Submit Food Intake"}
          </button>
        </form>

        {/* Medication Entry */}
        <form onSubmit={handleSubmitMed} className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Medication Entry</h2>
          <div className="flex flex-col space-y-4">
            <input type="text" placeholder="Insulin Name" value={medName} onChange={(e) => setMedName(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="number" placeholder="Dosage (units)" value={dosage} onChange={(e) => setDosage(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="datetime-local" value={medTime} onChange={(e) => setMedTime(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
          </div>
          <button type="submit" className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${medButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`}
            style={{ color: '#FCEDE9' }}>
            {medButtonPressed ? "Reupload File" : "Submit Medication Entry"}
          </button>
        </form>

        {/* Activity Entry */}
        <form onSubmit={handleSubmitActivity} className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Activity Entry</h2>
          <div className="flex flex-col space-y-4">
            <input type="text" placeholder="Activity Type" value={activityType} onChange={(e) => setActivityType(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="number" placeholder="Duration (minutes)" value={duration} onChange={(e) => setDuration(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <select value={intensity} onChange={(e) => setIntensity(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }}>
              <option value="">Intensity</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
          <button type="submit" className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${activityButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`}
            style={{ color: '#FCEDE9' }}>
            {activityButtonPressed ? "Reupload File" : "Submit Activity Entry"}
          </button>
        </form>

        {/* File Upload for Steps CSV */}
        <div className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Upload Steps File</h2>
          <input type="file" accept=".csv" onChange={handleFileChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />

          {/* Date Range Selection */}
          <div className="flex space-x-4 mt-4">
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-4 py-2 rounded-md border border-gray-300" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
          </div>

          <button type="button" onClick={handleProcessCSV}
            className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${csvButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`}
            style={{ color: '#FCEDE9' }}>
            {csvButtonPressed ? "Reupload File" : "Process CSV and Display Graph"}
          </button>
        </div>

        {/* Display the graph image if available */}
        {graphImage && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold" style={{ color: '#2D799C' }}>Steps Over Time</h2>
            <img src={graphImage} alt="Steps Over Time Graph" className="mt-4 rounded-lg shadow-md" />
          </div>
        )}

        {/* ECG Analysis Section */}
        <div className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Upload ECG File</h2>
          <input type="file" accept=".csv" onChange={handleEcgFileChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
          <button onClick={handleAnalyzeECG} disabled={loading}
            className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${ecgButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`}
            style={{ color: '#FCEDE9' }}>
            {loading ? "Analyzing..." : ecgButtonPressed ? "Reupload File" : "Analyze ECG"}
          </button>
        </div>

        {/* Display the ECG graph image if available */}
        {ecgGraphImage && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold" style={{ color: '#2D799C' }}>ECG Signal with Detected QRS Complexes</h2>
            <img src={ecgGraphImage} alt="ECG Signal Graph" className="mt-4 rounded-lg shadow-md" />
          </div>
        )}

        {/* Eye Fundus Image Upload */}
        <div className="mb-8 p-6 rounded-lg shadow-md" style={{ backgroundColor: '#E8F4F8' }}>
          <h2 className="text-2xl font-semibold mb-4" style={{ color: '#2D799C' }}>Upload Eye Fundus Image</h2>
          <input type="file" accept=".png" onChange={handleEyeFundusFileChange} className="w-full px-4 py-2 border border-gray-300 rounded-md" style={{ backgroundColor: '#FFFFFF', color: '#2D799C' }} />
          <button onClick={handleUploadEyeFundus} disabled={loading} className={`w-full mt-4 px-4 py-2 font-semibold rounded-md ${eyeFundusButtonPressed ? 'bg-green-500' : 'bg-blue-700'}`} style={{ color: '#FCEDE9' }}>
            {loading ? "Uploading..." : eyeFundusButtonPressed ? "Reupload Image" : "Upload Eye Fundus Image"}
          </button>
        </div>

        {/* Display the Eye Fundus Image if available */}
        {eyeFundusImage && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold" style={{ color: '#2D799C' }}>Eye Fundus Image</h2>
            <img src={eyeFundusImage} alt="Eye Fundus Image" className="mt-4 rounded-lg shadow-md" />
          </div>
        )}

        {/* Create Report Button */}
        <button type="button" className="w-full mt-8 px-4 py-2 font-semibold rounded-md"
          style={{ backgroundColor: '#16384F', color: '#FCEDE9' }}
          onClick={handleToggleReport}
        >
          {showReport ? "Hide Report" : "View Report"}
        </button>
        {/* PDF Viewer Section */}
        {showReport && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold" style={{ color: '#2D799C' }}>Report Preview</h2>
            <iframe
              src="/sugarsense.pdf"
              width="100%"
              height="600px"
              style={{ border: '1px solid #2D799C', marginTop: '16px' }}
              title="Sugarsense Output PDF"
            ></iframe>
          </div>
        )}
      </div>
    </div>
  );
}

