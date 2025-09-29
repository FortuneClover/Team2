import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter,Routes,Route } from 'react-router-dom';
import './index.css'
import App from './App.jsx'
import Write from './Write'
import Login from './login'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/app" element={<App />} />
        <Route path="/write" element={<Write />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
