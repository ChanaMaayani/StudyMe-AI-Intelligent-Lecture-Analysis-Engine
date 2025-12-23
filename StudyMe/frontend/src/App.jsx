// import { useState } from 'react'
// import axios from 'axios'
// import './App.css'

// function App() {
//   const [file, setFile] = useState(null)
//   const [result, setResult] = useState(null)
//   const [loading, setLoading] = useState(false)

//   const handleUpload = async () => {
//     if (!file) return alert("אנא בחרי קובץ אודיו")
    
//     setLoading(true)
//     const formData = new FormData()
//     formData.append('file', file)

//     try {
//       // שליחת הקובץ לשרת הפייתון שלנו
//       const response = await axios.post('http://localhost:8000/analyze', formData)
//       setResult(response.data)
//     } catch (error) {
//       console.error("Error uploading file:", error)
//       alert("משהו השתבש בניתוח הקובץ")
//     } finally {
//       setLoading(false)
//     }
//   }

//   return (
//     <div className="container">
//       <h1>StudyMe 🎓</h1>
//       <p>העלי את הקלטת השיעור וקבלי סיכום ושאלות לתרגול</p>
      
//       <div className="upload-section">
//         <input type="file" accept="audio/*" onChange={(e) => setFile(e.target.files[0])} />
//         <button onClick={handleUpload} disabled={loading}>
//           {loading ? "מנתח נתונים..." : "נתח שיעור"}
//         </button>
//       </div>

//       {result && (
//         <div className="results">
//           <h2>סיכום השיעור:</h2>
//           <p>{result.summary || "הקובץ התקבל בשרת בהצלחה!"}</p>
//           {/* כאן נוסיף בהמשך את השאלות והמשימות */}
//         </div>
//       )}
//     </div>
//   )
// }

// export default App
// App.jsx

import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [quizAnswers, setQuizAnswers] = useState({})
  const [showScore, setShowScore] = useState(false)

  const handleUpload = async () => {
    if (!file) return alert("נא לבחור קובץ תחילה")
    
    setLoading(true)
    setResult(null)
    setQuizAnswers({})
    setShowScore(false)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:9000/analyze', formData)
      setResult(response.data)
    } catch (error) {
      console.error("Error:", error)
      alert("הייתה בעיה בעיבוד הקובץ, ודאי שהשרת פועל")
    } finally {
      setLoading(false)
    }
  }

  const handleQuizSelect = (qIndex, option) => {
    setQuizAnswers({ ...quizAnswers, [qIndex]: option })
  }

  const calculateScore = () => {
    if (!result?.quiz) return 0
    let correct = 0
    result.quiz.forEach((q, i) => {
      if (quizAnswers[i] === q.answer) correct++
    })
    return Math.round((correct / result.quiz.length) * 100)
  }

  return (
    <div className="app-wrapper">
      <div className="glass-container">
        
        <header className="header">
          <h1 className="logo">StudyMe 🎓</h1>
          <p className="subtitle">המורה הפרטי שלך לסיכום שיעורים, הכנת שיעורי בית ומבחנים</p>
        </header>

        <div className="upload-zone">
          <div className="file-input-wrapper">
            <input 
              type="file" 
              id="file"
              accept="audio/*,video/*"
              onChange={(e) => setFile(e.target.files[0])} 
            />
            <label htmlFor="file" className="file-label">
              <span className="icon">{file ? "✅" : "☁️"}</span>
              <span className="text">{file ? file.name : "גרירת קובץ אודיו/וידאו לכאן"}</span>
            </label>
          </div>
          
          <button className="cta-button" onClick={handleUpload} disabled={loading || !file}>
            {loading ? (
              <>
                <div className="loader"></div>
                <span>מעבד את הקובץ...</span>
              </>
            ) : (
              <>
                <span>🚀</span>
                <span>התחל ניתוח חכם</span>
              </>
            )}
          </button>
        </div>

        {result && (
          <div className="content-stack">
            
            {/* סיכום */}
            <div className="glass-card">
              <div className="card-header">
                <span>📝</span>
                <span>סיכום השיעור</span>
              </div>
              <p className="summary-text">{result.summary}</p>
              {result.key_points?.length > 0 && (
                <div className="tags-container">
                  {result.key_points.map((point, i) => (
                    <span key={i} className="tag">#{point}</span>
                  ))}
                </div>
              )}
            </div>

            {/* משימות */}
            <div className="glass-card">
              <div className="card-header">
                <span>⚡</span>
                <span>משימות לביצוע</span>
              </div>
              {result.tasks?.length > 0 ? (
                <ul className="custom-checklist">
                  {result.tasks.map((task, i) => (
                    <li key={i}>
                      <input type="checkbox" id={`task-${i}`} />
                      <label htmlFor={`task-${i}`}>{task}</label>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>אין משימות מיוחדות לשיעור זה 🎉</p>
              )}
            </div>

            {/* מבחן */}
            <div className="glass-card">
              <div className="card-header">
                <span>🧠</span>
                <span>בחן את עצמך</span>
              </div>
              
              {!showScore ? (
                <>
                  {result.quiz?.map((q, i) => (
                    <div key={i} className="quiz-item">
                      <p className="question">{i + 1}. {q.question}</p>
                      <div className="options">
                        {q.options.map((opt, optI) => (
                          <button 
                            key={optI}
                            className={`option-btn ${quizAnswers[i] === opt ? 'selected' : ''}`}
                            onClick={() => handleQuizSelect(i, opt)}
                          >
                            {opt}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                  <button className="cta-button" style={{width: '100%', marginTop: '20px'}} onClick={() => setShowScore(true)}>
                    <span>🏆</span>
                    <span>הגש מבחן וקבל ציון</span>
                  </button>
                </>
              ) : (
                <div className="score-badge">
                  <div>הציון שלך: {calculateScore()}%</div>
                  <button onClick={() => {setShowScore(false); setQuizAnswers({})}}>
                    נסה שוב 🔄
                  </button>
                </div>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  )
}

export default App