import React, { useState } from 'react';
import './App.css';

// API base URL:
// - In development: use REACT_APP_API_URL or fallback to local FastAPI backend
// - In production: prefer REACT_APP_API_URL so we can point to an external backend (Railway/Render)
const API_URL =
  process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'https://your-backend-url-here' // override via Netlify env
    : 'http://localhost:8000');

function App() {
  const [activePage, setActivePage] = useState('predict');
  const [selectedModel, setSelectedModel] = useState('');
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [leftImage, setLeftImage] = useState(null);
  const [leftPreview, setLeftPreview] = useState(null);
  const [rightImage, setRightImage] = useState(null);
  const [rightPreview, setRightPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showResult, setShowResult] = useState(false);

  const models = [
    { 
      id: 'hypertension', 
      name: 'Hypertension Detection', 
      description: 'Binary classification (0 or 1)', 
      color: '#ff6b6b',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
      )
    },
    { 
      id: 'cimt', 
      name: 'CIMT Regression', 
      description: 'Carotid Intima-Media Thickness (0.4 - 1.2)', 
      color: '#4ecdc4',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <path d="M3 6h3a6 6 0 0 1 6 6 6 6 0 0 1 6-6h3"/>
        </svg>
      )
    },
    { 
      id: 'vessel', 
      name: 'A/V Segmentation', 
      description: 'Arterial/Venous vessel masking', 
      color: '#95e1d3',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
        </svg>
      )
    },
    { 
      id: 'fusion', 
      name: 'Fusion Model', 
      description: 'Combined CVD risk prediction', 
      color: '#f38181',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L2 7l10 5 10-5-10-5z"/>
          <path d="M2 17l10 5 10-5"/>
          <path d="M2 12l10 5 10-5"/>
        </svg>
      )
    }
  ];

  const handleImageChange = (e, side = 'single') => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        if (side === 'left') {
          setLeftImage(file);
          setLeftPreview(reader.result);
        } else if (side === 'right') {
          setRightImage(file);
          setRightPreview(reader.result);
        } else {
          setImage(file);
        setPreview(reader.result);
        }
      };
      reader.readAsDataURL(file);
      setResult(null);
      setError(null);
      setShowResult(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedModel) {
      setError('Please select a model');
      return;
    }
    
    // Check if model needs 2 images (CIMT, Fusion) or 1 image (Hypertension, Vessel)
    const needsTwoImages = selectedModel === 'cimt' || selectedModel === 'fusion';
    
    if (needsTwoImages) {
      if (!leftImage || !rightImage) {
        setError('Please upload both left and right eye images');
        return;
      }
    } else {
    if (!image) {
      setError('Please upload an image');
      return;
      }
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setShowResult(false);

    const formData = new FormData();
    formData.append('model', selectedModel);
    
    if (needsTwoImages) {
      formData.append('left_image', leftImage);
      formData.append('right_image', rightImage);
    } else {
      formData.append('image', image);
    }

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = 'Prediction failed';
        try {
        const errorData = await response.json();
          if (errorData.detail) {
            errorMessage = typeof errorData.detail === 'string' 
              ? errorData.detail 
              : JSON.stringify(errorData.detail);
          } else if (errorData.message) {
            errorMessage = typeof errorData.message === 'string'
              ? errorData.message
              : JSON.stringify(errorData.message);
          }
        } catch (parseError) {
          errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setResult(data);
      setTimeout(() => setShowResult(true), 100);
    } catch (err) {
      const errorMessage = err instanceof Error 
        ? err.message 
        : typeof err === 'string' 
        ? err 
        : JSON.stringify(err);
      setError(errorMessage || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setPreview(null);
    setLeftImage(null);
    setLeftPreview(null);
    setRightImage(null);
    setRightPreview(null);
    setSelectedModel('');
    setResult(null);
    setError(null);
    setShowResult(false);
  };
  
  const handleResetSide = (side) => {
    if (side === 'left') {
      setLeftImage(null);
      setLeftPreview(null);
    } else if (side === 'right') {
      setRightImage(null);
      setRightPreview(null);
    }
    setResult(null);
    setError(null);
    setShowResult(false);
  };
  
  // Check if model needs 2 images
  const needsTwoImages = selectedModel === 'cimt' || selectedModel === 'fusion';

  const getButtonText = () => {
    if (loading) return 'Processing...';
    const model = models.find(m => m.id === selectedModel);
    if (model) {
      if (model.id === 'hypertension') return 'Predict Hypertension';
      if (model.id === 'cimt') return 'Predict CIMT Value';
      if (model.id === 'vessel') return 'Run A/V Segmentation';
      if (model.id === 'fusion') return 'Run Fusion Model';
    }
    return 'Select a Model';
  };

  return (
    <div className="App">
      <div className="background-gradient"></div>
      <div className="container">
        <header className="header">
          <div className="header-content">
            <h1 className="title">
              <span className="title-gradient">CVD Risk Predictor</span>
            </h1>
            <p className="subtitle">AI-Powered Cardiovascular Disease Risk Assessment from Retinal Images</p>
          </div>
        </header>

        <div className="main-content glass-card">
          <nav className="top-nav">
            {[
              { 
                id: 'predict', 
                label: 'Prediction',
                icon: (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                  </svg>
                )
              },
              { 
                id: 'background', 
                label: 'Medical Background',
                icon: (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                )
              },
              { 
                id: 'models', 
                label: 'Model Overview',
                icon: (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="7" height="7"/>
                    <rect x="14" y="3" width="7" height="7"/>
                    <rect x="14" y="14" width="7" height="7"/>
                    <rect x="3" y="14" width="7" height="7"/>
                  </svg>
                )
              },
              { 
                id: 'team', 
                label: 'Team',
                icon: (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                )
              }
            ].map((page) => (
              <button
                key={page.id}
                type="button"
                className={`nav-link ${activePage === page.id ? 'active' : ''}`}
                onClick={() => setActivePage(page.id)}
              >
                <span className="nav-icon">{page.icon}</span>
                {page.label}
              </button>
            ))}
          </nav>

          {activePage === 'predict' && (
            <div className="page-content fade-in">
          <form onSubmit={handleSubmit} className="upload-section">
            <div className="model-selection">
                  <h2 className="section-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M12 6v6l4 2"/>
                    </svg>
                    Select Model
                  </h2>
              <div className="model-grid">
                    {models.map((model, index) => (
                  <div
                    key={model.id}
                    className={`model-card ${selectedModel === model.id ? 'selected' : ''}`}
                        style={{ '--model-color': model.color }}
                    onClick={() => {
                      setSelectedModel(model.id);
                      setError(null);
                    }}
                  >
                        <div className="model-icon-wrapper" style={{ color: model.color }}>
                          {model.icon}
                    </div>
                    <h3>{model.name}</h3>
                    <p>{model.description}</p>
                        {selectedModel === model.id && (
                          <div className="selected-indicator">Selected</div>
                        )}
                  </div>
                ))}
              </div>
            </div>

            <div className="image-upload">
                  <h2 className="section-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    {needsTwoImages ? 'Upload Retinal Images (Both Eyes)' : 'Upload Retinal Image'}
                  </h2>
                  
                  {needsTwoImages ? (
                    <div className="dual-upload-container">
                      <div className="upload-area">
                        <div className="upload-label-text">Left Eye</div>
                        {leftPreview ? (
                          <div className="image-preview">
                            <img src={leftPreview} alt="Left Eye Preview" className="preview-img" />
                            <button
                              type="button"
                              className="remove-image"
                              onClick={() => handleResetSide('left')}
                            >
                              ✕
                            </button>
                          </div>
                        ) : (
                          <label className="upload-label">
                            <input
                              type="file"
                              accept="image/*"
                              onChange={(e) => handleImageChange(e, 'left')}
                              className="file-input"
                            />
                            <div className="upload-content">
                              <div className="upload-icon">
                                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                  <polyline points="17 8 12 3 7 8" />
                                  <line x1="12" y1="3" x2="12" y2="15" />
                                </svg>
                              </div>
                              <p className="upload-text">Left Eye</p>
                              <span className="upload-hint">PNG, JPG, JPEG</span>
                            </div>
                          </label>
                        )}
                      </div>
                      
                      <div className="upload-area">
                        <div className="upload-label-text">Right Eye</div>
                        {rightPreview ? (
                          <div className="image-preview">
                            <img src={rightPreview} alt="Right Eye Preview" className="preview-img" />
                            <button
                              type="button"
                              className="remove-image"
                              onClick={() => handleResetSide('right')}
                            >
                              ✕
                            </button>
                          </div>
                        ) : (
                          <label className="upload-label">
                            <input
                              type="file"
                              accept="image/*"
                              onChange={(e) => handleImageChange(e, 'right')}
                              className="file-input"
                            />
                            <div className="upload-content">
                              <div className="upload-icon">
                                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                  <polyline points="17 8 12 3 7 8" />
                                  <line x1="12" y1="3" x2="12" y2="15" />
                                </svg>
                              </div>
                              <p className="upload-text">Right Eye</p>
                              <span className="upload-hint">PNG, JPG, JPEG</span>
                            </div>
                          </label>
                        )}
                      </div>
                    </div>
                  ) : (
              <div className="upload-area">
                {preview ? (
                  <div className="image-preview">
                          <img src={preview} alt="Preview" className="preview-img" />
                    <button
                      type="button"
                      className="remove-image"
                      onClick={handleReset}
                    >
                            ✕
                    </button>
                  </div>
                ) : (
                  <label className="upload-label">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                      className="file-input"
                    />
                    <div className="upload-content">
                            <div className="upload-icon">
                              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                            </div>
                            <p className="upload-text">Click to upload or drag and drop</p>
                            <span className="upload-hint">PNG, JPG, JPEG up to 10MB</span>
                    </div>
                  </label>
                )}
              </div>
                  )}
            </div>

            {error && (
                  <div className="error-message slide-in">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="error-icon">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="8" x2="12" y2="12"/>
                      <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              className="submit-button"
                  disabled={loading || !selectedModel || (needsTwoImages ? (!leftImage || !rightImage) : !image)}
            >
              {loading ? (
                <>
                      <div className="spinner"></div>
                      <span>Processing...</span>
                </>
              ) : (
                    <>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="button-icon">
                        <polyline points="5 12 3 12 12 3 21 12 19 12"/>
                        <polyline points="19 12 19 21 5 21 5 12"/>
                      </svg>
                      <span>{getButtonText()}</span>
                    </>
              )}
            </button>
          </form>

          {result && (
                <div className={`result-section ${showResult ? 'show' : ''}`}>
                  <h2 className="section-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                    </svg>
                    Prediction Results
                  </h2>
              <div className="result-card">
                {selectedModel === 'hypertension' && (
                  <div className="result-content">
                    <div className="result-label">Hypertension Prediction</div>
                    <div className={`result-value ${result.prediction === 1 ? 'positive' : 'negative'}`}>
                      {result.prediction === 1 ? 'Positive (1)' : 'Negative (0)'}
                    </div>
                    {result.confidence && (
                          <div className="confidence-bar">
                            <div className="confidence-label">Confidence</div>
                            <div className="confidence-track">
                              <div 
                                className="confidence-fill"
                                style={{ width: `${result.confidence * 100}%` }}
                              ></div>
                            </div>
                            <div className="confidence-value">{(result.confidence * 100).toFixed(2)}%</div>
                      </div>
                    )}
                  </div>
                )}

                {selectedModel === 'cimt' && (
                  <div className="result-content">
                    <div className="result-label">CIMT Value</div>
                        <div className="result-value cimt-value">
                      {result.prediction?.toFixed(4) || result.value?.toFixed(4)}
                    </div>
                    <div className="result-description">
                      Carotid Intima-Media Thickness (mm)
                    </div>
                  </div>
                )}

                {selectedModel === 'vessel' && (
                      <div className="result-content vessel-result">
                    <div className="result-label">Segmented Vessels</div>
                    {result.masked_image && (
                      <div className="masked-image">
                        <img
                          src={`data:image/png;base64,${result.masked_image}`}
                          alt="Segmented vessels"
                              className="vessel-mask"
                        />
                      </div>
                    )}
                        {result.features && (
                          <div className="vessel-features">
                            <h3 className="features-title">Vessel Features</h3>
                            <div className="features-grid">
                              {Object.entries(result.features).map(([key, value], idx) => (
                                <div className="feature-item" key={key} style={{ animationDelay: `${idx * 0.05}s` }}>
                                  <span className="feature-label">
                                    {key.replace('vessel_', 'Vessel ').replace('percentile_', 'Percentile ').replace(/_/g, ' ')}
                                  </span>
                                  <span className="feature-value">
                                    {typeof value === 'number' ? value.toFixed(4) : String(value)}
                                  </span>
                                </div>
                              ))}
                            </div>
                      </div>
                    )}
                  </div>
                )}

                {selectedModel === 'fusion' && (
                      <div className="result-content fusion-result">
                    <div className="result-label">Fusion Model Prediction</div>
                        <div className="fusion-main">
                          <div className="fusion-prediction">
                            <span className="fusion-label">Risk Level</span>
                            <span className={`fusion-value ${result.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
                              {result.prediction === 1 ? 'High Risk' : 'Low Risk'}
                            </span>
                          </div>
                          {result.probability !== undefined && (
                            <div className="fusion-probability">
                              <span className="prob-label">Probability</span>
                              <span className="prob-value">{(result.probability * 100).toFixed(2)}%</span>
                            </div>
                          )}
                    </div>
                    {result.components && (
                      <div className="fusion-components">
                            <h3 className="components-title">Component Predictions</h3>
                            <div className="components-grid">
                              <div className="component-card">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="component-icon">
                                  <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                                </svg>
                                <div className="component-info">
                                  <span className="component-label">Hypertension</span>
                                  <span className="component-value">{result.components.hypertension}</span>
                                </div>
                              </div>
                              <div className="component-card">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="component-icon">
                                  <line x1="3" y1="12" x2="21" y2="12"/>
                                  <path d="M3 6h3a6 6 0 0 1 6 6 6 6 0 0 1 6-6h3"/>
                                </svg>
                                <div className="component-info">
                                  <span className="component-label">CIMT</span>
                                  <span className="component-value">{result.components.cimt?.toFixed(4)}</span>
                                </div>
                              </div>
                              <div className="component-card">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="component-icon">
                                  <circle cx="12" cy="12" r="10"/>
                                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                                </svg>
                                <div className="component-info">
                                  <span className="component-label">Vessel Density</span>
                                  <span className="component-value">
                                    {result.components.vessel_density !== undefined
                                      ? result.components.vessel_density.toFixed(4)
                                      : 'N/A'}
                                  </span>
                                </div>
                        </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
                  </div>
                </div>
              )}
            </div>
          )}

          {activePage === 'background' && (
            <div className="page-content info-section fade-in">
              <h2 className="section-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
                Why This Project Matters
              </h2>
              <div className="info-card highlight-card">
                <p>
                  Cardiovascular diseases (CVDs) are the leading cause of death worldwide, responsible for
                  roughly one in three deaths each year. Many heart attacks and strokes happen
                  prematurely, often before age 70, and much of this burden is preventable with earlier
                  risk detection and intervention.
                </p>
                <p>
                  Because CVD usually develops silently over many years, tools that can flag higher risk
                  before symptoms appear are crucial. Retinal imaging offers a non-invasive, widely
                  available way to look at the body&apos;s small blood vessels, providing an additional
                  window into vascular health alongside traditional risk factors like blood pressure or
                  cholesterol.
                </p>
              </div>

              <h2 className="section-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                Medical Background
              </h2>
              <div className="info-grid">
                {[
                  {
                    title: 'Cardiovascular Disease & Atherosclerosis',
                    content: 'Atherosclerosis is a slow process where fatty deposits build up inside artery walls, causing them to thicken and narrow. This can eventually limit blood flow or lead to clots that trigger heart attacks and strokes.'
                  },
                  {
                    title: 'Hypertension & Microvasculature',
                    content: 'Long-standing high blood pressure puts extra strain on blood vessels, especially the tiny vessels that supply organs. Over time this can make vessels stiffer and more fragile, increasing the risk of damage to the heart, brain, kidneys and eyes.'
                  },
                  {
                    title: 'Carotid Intima–Media Thickness (CIMT)',
                    content: 'CIMT measures the thickness of the inner layers of the carotid artery in the neck. Higher CIMT values are linked with a higher chance of future cardiovascular events and are often viewed as an early marker of atherosclerosis.'
                  },
                  {
                    title: 'Retinal Vessels & Systemic Health',
                    content: 'The retina is one of the few places where doctors can directly see blood vessels without surgery. Subtle changes in vessel width, shape and branching can reflect broader vascular stress elsewhere in the body.'
                  }
                ].map((item, idx) => (
                  <div key={idx} className="info-card" style={{ animationDelay: `${idx * 0.1}s` }}>
                    <h3>{item.title}</h3>
                    <p>{item.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activePage === 'models' && (
            <div className="page-content info-section fade-in">
              <h2 className="section-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                  <rect x="3" y="3" width="7" height="7"/>
                  <rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/>
                  <rect x="3" y="14" width="7" height="7"/>
                </svg>
                Model Overview
              </h2>
              <div className="info-grid">
                {[
                  {
                    title: 'Hypertension Detection',
                    content: 'A vision transformer-based model analyzes a single retinal image and predicts the likelihood of hypertension, using patterns in vessel appearance and overall image features learned from large datasets.'
                  },
                  {
                    title: 'CIMT Regression',
                    content: 'A siamese multimodal network processes left and right eye images together with basic clinical inputs to estimate carotid intima–media thickness, a surrogate marker of arterial wall health.'
                  },
                  {
                    title: 'A/V Vessel Segmentation',
                    content: 'A U-Net style segmentation model highlights the retinal vessel tree, producing a binary mask that separates vessels from background and enables simple measures like vessel density.'
                  },
                  {
                    title: 'Fusion CVD Risk Model',
                    content: 'A meta-classifier combines features from all three base models into a single risk score, integrating information about hypertension, vessel structure and estimated arterial wall thickness.'
                  }
                ].map((item, idx) => (
                  <div key={idx} className="info-card model-info-card" style={{ animationDelay: `${idx * 0.1}s` }}>
                    <h3>{item.title}</h3>
                    <p>{item.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activePage === 'team' && (
            <div className="page-content info-section fade-in">
              <h2 className="section-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="title-icon">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                Project Team
              </h2>
              <div className="info-card team-card">
                <div className="team-members">
                  {['Karim Abdalla', 'Carl Wakim', 'Hussein Mdaihly', 'Hassan Hashem'].map((name, idx) => (
                    <div key={idx} className="team-member" style={{ animationDelay: `${idx * 0.1}s` }}>
                      <div className="member-avatar">{name.split(' ').map(n => n[0]).join('')}</div>
                      <span className="member-name">{name}</span>
                    </div>
                  ))}
                </div>
                <p className="team-description">
                  This project was developed as part of an academic effort to explore deep learning for non-invasive cardiovascular risk assessment.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
