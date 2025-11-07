import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import VerifyEmail from './pages/VerifyEmail'
import Profile from './pages/Profile'
import Matches from './pages/Matches'
import DateRequests from './pages/DateRequests'
import Events from './pages/Events'
import Messages from './pages/Messages'
import Layout from './components/Layout'
import PageTransition from './components/PageTransition'

// Protected Route component
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function AppRoutes() {
  const location = useLocation()
  
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={
          <PageTransition>
            <Home />
          </PageTransition>
        } />
        <Route path="/login" element={
          <PageTransition>
            <Login />
          </PageTransition>
        } />
        <Route path="/register" element={
          <PageTransition>
            <Register />
          </PageTransition>
        } />
        <Route path="/verify-email" element={
          <PageTransition>
            <VerifyEmail />
          </PageTransition>
        } />
        
        <Route path="/app" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Navigate to="/app/profile" replace />} />
          <Route path="profile" element={
            <PageTransition>
              <Profile />
            </PageTransition>
          } />
          <Route path="matches" element={
            <PageTransition>
              <Matches />
            </PageTransition>
          } />
          <Route path="date-requests" element={
            <PageTransition>
              <DateRequests />
            </PageTransition>
          } />
          <Route path="events" element={
            <PageTransition>
              <Events />
            </PageTransition>
          } />
          <Route path="messages" element={
            <PageTransition>
              <Messages />
            </PageTransition>
          } />
        </Route>
      </Routes>
    </AnimatePresence>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  )
}

export default App

