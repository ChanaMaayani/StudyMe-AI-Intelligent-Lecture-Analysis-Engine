import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!file) return alert("אנא בחרי קובץ אודיו")
    
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      // שליחת הקובץ לשרת הפייתון שלנו
      const response = await axios.post('http://localhost:8000/analyze', formData)
      setResult(response.data)
    } catch (error) {
      console.error("Error uploading file:", error)
      alert("משהו השתבש בניתוח הקובץ")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>StudyMe 🎓</h1>
      <p>העלי את הקלטת השיעור וקבלי סיכום ושאלות לתרגול</p>
      
      <div className="upload-section">
        <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "מנתח נתונים..." : "נתח שיעור"}
        </button>
      </div>

      {result && (
        <div className="results">
          <h2>סיכום השיעור:</h2>
          <p>{result.summary || "הקובץ התקבל בשרת בהצלחה!"}</p>
          {/* כאן נוסיף בהמשך את השאלות והמשימות */}
        </div>
      )}
    </div>
  )
}

export default App