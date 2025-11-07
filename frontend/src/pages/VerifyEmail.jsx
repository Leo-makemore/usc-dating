import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function VerifyEmail() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [status, setStatus] = useState('verifying')
  const [message, setMessage] = useState('')

  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      verifyToken(token)
    } else {
      setStatus('error')
      setMessage('No verification token provided')
    }
  }, [searchParams])

  const verifyToken = async (token) => {
    try {
      await api.post('/api/auth/verify-email', { token })
      setStatus('success')
      setMessage('Email verified successfully! You can now login.')
    } catch (error) {
      setStatus('error')
      setMessage(error.response?.data?.detail || 'Verification failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          {status === 'verifying' && (
            <>
              <h2 className="text-3xl font-extrabold text-gray-900">Verifying Email...</h2>
              <p className="mt-2 text-gray-600">Please wait</p>
            </>
          )}
          {status === 'success' && (
            <>
              <div className="text-green-500 text-5xl mb-4">✓</div>
              <h2 className="text-3xl font-extrabold text-gray-900">Email Verified!</h2>
              <p className="mt-2 text-gray-600">{message}</p>
              <button
                onClick={() => navigate('/login')}
                className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-md"
              >
                Go to Login
              </button>
            </>
          )}
          {status === 'error' && (
            <>
              <div className="text-red-500 text-5xl mb-4">✗</div>
              <h2 className="text-3xl font-extrabold text-gray-900">Verification Failed</h2>
              <p className="mt-2 text-red-600">{message}</p>
              <button
                onClick={() => navigate('/login')}
                className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-md"
              >
                Go to Login
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

