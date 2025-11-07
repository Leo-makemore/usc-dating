import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../services/api'

export default function Register() {
  const [step, setStep] = useState(0) // 0: Account (email/password), 1: Profile
  const [step1Data, setStep1Data] = useState({ email: '', password: '', confirmPassword: '' })
  const [step2Data, setStep2Data] = useState({
    name: '',
    school: 'University of Southern California',
    year: '',
    interests: '',
    height_cm: '',
    weight_kg: '',
    nationality: '',
    ethnicity: '',
    photos: []
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [tempToken, setTempToken] = useState('')
  const navigate = useNavigate()

  const handleStep1Submit = async (e) => {
    e.preventDefault()
    setError('')
    
    // Validation
    if (!step1Data.email.endsWith('.edu')) {
      setError('Only university email addresses (.edu domain) are allowed')
      return
    }
    
    if (step1Data.password.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }
    
    if (step1Data.password !== step1Data.confirmPassword) {
      setError('Passwords do not match')
      return
    }
    
    setLoading(true)

    try {
      const response = await api.post('/api/auth/register-step1', {
        email: step1Data.email,
        password: step1Data.password
      })
      
      console.log('Step 1 response:', response.data)
      
      if (!response.data.temp_token) {
        throw new Error('No temp token received from server')
      }
      
      setTempToken(response.data.temp_token)
      console.log('Temp token saved:', response.data.temp_token.substring(0, 20) + '...')
      
      // Auto-fill school based on email domain
      const emailDomain = step1Data.email.split('@')[1].toLowerCase()
      if (emailDomain === 'usc.edu') {
        setStep2Data({ ...step2Data, school: 'University of Southern California' })
      }
      
      setStep(1)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create account')
    } finally {
      setLoading(false)
    }
  }

  const handleStep2Submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!tempToken) {
        setError('Registration session expired. Please start over.')
        setStep(0)
        return
      }
      
      console.log('Submitting step 2 with temp token:', tempToken.substring(0, 20) + '...')
      
      const interestsArray = step2Data.interests
        .split(',')
        .map((i) => i.trim())
        .filter((i) => i.length > 0)

      const response = await api.post('/api/auth/register-step2', {
        ...step2Data,
        interests: interestsArray,
        height_cm: step2Data.height_cm ? parseInt(step2Data.height_cm) : null,
        weight_kg: step2Data.weight_kg ? parseInt(step2Data.weight_kg) : null
      }, {
        headers: {
          'Authorization': `Bearer ${tempToken}`
        }
      })
      
      console.log('Step 2 response:', response.data)
      
      // Store token and navigate
      const accessToken = response.data.access_token
      if (!accessToken) {
        throw new Error('No access token received from server')
      }
      
      localStorage.setItem('token', accessToken)
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      
      // Wait a bit to ensure token is set, then navigate
      setTimeout(() => {
        navigate('/app/matches')
      }, 100)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to complete registration')
    } finally {
      setLoading(false)
    }
  }

  const slideVariants = {
    enter: (direction) => ({
      x: direction > 0 ? 1000 : -1000,
      opacity: 0
    }),
    center: {
      x: 0,
      opacity: 1
    },
    exit: (direction) => ({
      x: direction < 0 ? 1000 : -1000,
      opacity: 0
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-neutral-900 to-black text-white flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-900/20 via-blue-900/20 to-pink-900/20 animate-pulse"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent)]"></div>
      
      <div className="w-full max-w-2xl relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="mb-8">
            <Link 
              to="/" 
              className="text-neutral-400 hover:text-white transition-all duration-300 text-sm inline-flex items-center group"
            >
              <motion.span
                className="mr-2 group-hover:-translate-x-1 transition-transform duration-300"
                whileHover={{ x: -4 }}
              >
                ←
              </motion.span>
              Back to home
            </Link>
          </div>
        </motion.div>

        {/* Progress indicator */}
        <motion.div 
          className="mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`flex items-center transition-all duration-500 ${step >= 0 ? 'text-white' : 'text-neutral-600'}`}>
              <motion.div 
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all duration-500 ${
                  step >= 0 ? 'bg-gradient-to-br from-white to-neutral-200 text-black shadow-lg' : 'bg-neutral-800'
                }`}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                {step > 0 ? '✓' : '1'}
              </motion.div>
              <span className="ml-3 text-sm font-medium">Account</span>
            </div>
            <motion.div 
              className={`flex-1 h-1 mx-4 rounded-full transition-all duration-500 ${
                step >= 1 ? 'bg-gradient-to-r from-white to-white' : 'bg-neutral-800'
              }`}
              initial={{ scaleX: 0 }}
              animate={{ scaleX: step >= 1 ? 1 : 0 }}
              transition={{ duration: 0.5 }}
            ></motion.div>
            <div className={`flex items-center transition-all duration-500 ${step >= 1 ? 'text-white' : 'text-neutral-600'}`}>
              <motion.div 
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all duration-500 ${
                  step >= 1 ? 'bg-gradient-to-br from-white to-neutral-200 text-black shadow-lg' : 'bg-neutral-800'
                }`}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                2
              </motion.div>
              <span className="ml-3 text-sm font-medium">Profile</span>
            </div>
          </div>
        </motion.div>

        <AnimatePresence mode="wait" custom={step}>
          {step === 0 && (
            <motion.div
              key="step0"
              custom={0}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.3, ease: "easeInOut" }}
            >
              <div className="mb-8">
                <motion.h1 
                  className="text-4xl font-bold mb-3 bg-gradient-to-r from-white via-neutral-200 to-neutral-400 bg-clip-text text-transparent"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  Create Account
                </motion.h1>
                <motion.p 
                  className="text-neutral-400"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  Use your university email to get started
                </motion.p>
              </div>

              {error && (
                <motion.div 
                  className="mb-6 p-4 bg-red-950/50 border border-red-800/50 rounded-lg text-red-200 text-sm backdrop-blur-sm"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {error}
                </motion.div>
              )}

              <form onSubmit={handleStep1Submit} className="space-y-6">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <label htmlFor="email" className="block text-sm font-medium mb-2">
                    University Email *
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                    placeholder="your.email@usc.edu"
                    value={step1Data.email}
                    onChange={(e) => setStep1Data({ ...step1Data, email: e.target.value })}
                  />
                  <p className="mt-2 text-xs text-neutral-500">
                    Only .edu email addresses are allowed
                  </p>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <label htmlFor="password" className="block text-sm font-medium mb-2">
                    Password *
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    minLength={8}
                    className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                    placeholder="At least 8 characters"
                    value={step1Data.password}
                    onChange={(e) => setStep1Data({ ...step1Data, password: e.target.value })}
                  />
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <label htmlFor="confirmPassword" className="block text-sm font-medium mb-2">
                    Confirm Password *
                  </label>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    minLength={8}
                    className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                    placeholder="Confirm your password"
                    value={step1Data.confirmPassword}
                    onChange={(e) => setStep1Data({ ...step1Data, confirmPassword: e.target.value })}
                  />
                </motion.div>

                <motion.button
                  type="submit"
                  disabled={loading}
                  className="w-full px-4 py-3 bg-gradient-to-r from-white to-neutral-200 text-black rounded-lg font-medium hover:from-neutral-200 hover:to-neutral-300 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                  whileHover={{ scale: loading ? 1 : 1.02 }}
                  whileTap={{ scale: loading ? 1 : 0.98 }}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <motion.span
                        className="w-4 h-4 border-2 border-black border-t-transparent rounded-full mr-2"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      />
                      Creating account...
                    </span>
                  ) : (
                    'Continue'
                  )}
                </motion.button>
              </form>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div
              key="step1"
              custom={1}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.3, ease: "easeInOut" }}
            >
              <div className="mb-8">
                <motion.h1 
                  className="text-4xl font-bold mb-3 bg-gradient-to-r from-white via-neutral-200 to-neutral-400 bg-clip-text text-transparent"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  Complete your profile
                </motion.h1>
                <motion.p 
                  className="text-neutral-400"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.1 }}
                >
                  Tell us about yourself to find better matches
                </motion.p>
              </div>

              {error && (
                <motion.div 
                  className="mb-6 p-4 bg-red-950/50 border border-red-800/50 rounded-lg text-red-200 text-sm backdrop-blur-sm"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {error}
                </motion.div>
              )}

              <form onSubmit={handleStep2Submit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { id: 'name', label: 'Full Name *', required: true, value: step2Data.name, onChange: (e) => setStep2Data({ ...step2Data, name: e.target.value }) },
                    { id: 'school', label: 'School/University *', required: true, value: step2Data.school, onChange: (e) => setStep2Data({ ...step2Data, school: e.target.value }) },
                    { id: 'year', label: 'Year *', required: true, type: 'select', value: step2Data.year, onChange: (e) => setStep2Data({ ...step2Data, year: e.target.value }) },
                    { id: 'nationality', label: 'Nationality', value: step2Data.nationality, onChange: (e) => setStep2Data({ ...step2Data, nationality: e.target.value }) },
                    { id: 'height_cm', label: 'Height (cm)', type: 'number', value: step2Data.height_cm, onChange: (e) => setStep2Data({ ...step2Data, height_cm: e.target.value }) },
                    { id: 'weight_kg', label: 'Weight (kg)', type: 'number', value: step2Data.weight_kg, onChange: (e) => setStep2Data({ ...step2Data, weight_kg: e.target.value }) },
                    { id: 'ethnicity', label: 'Ethnicity', value: step2Data.ethnicity, onChange: (e) => setStep2Data({ ...step2Data, ethnicity: e.target.value }) },
                  ].map((field, index) => (
                    <motion.div
                      key={field.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * index }}
                    >
                      <label htmlFor={field.id} className="block text-sm font-medium mb-2">
                        {field.label}
                      </label>
                      {field.type === 'select' ? (
                        <select
                          id={field.id}
                          name={field.id}
                          required={field.required}
                          className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                          value={field.value}
                          onChange={field.onChange}
                        >
                          <option value="">Select year</option>
                          <option value="Freshman">Freshman</option>
                          <option value="Sophomore">Sophomore</option>
                          <option value="Junior">Junior</option>
                          <option value="Senior">Senior</option>
                          <option value="Graduate">Graduate</option>
                        </select>
                      ) : (
                        <input
                          id={field.id}
                          name={field.id}
                          type={field.type || 'text'}
                          required={field.required}
                          className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                          placeholder={field.placeholder}
                          value={field.value}
                          onChange={field.onChange}
                        />
                      )}
                    </motion.div>
                  ))}
                </div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                >
                  <label htmlFor="interests" className="block text-sm font-medium mb-2">
                    Interests (comma-separated)
                  </label>
                  <input
                    id="interests"
                    name="interests"
                    type="text"
                    className="w-full px-4 py-3 bg-neutral-900/50 backdrop-blur-sm border border-neutral-800 rounded-lg text-white placeholder-neutral-500 focus:outline-none focus:border-white focus:ring-2 focus:ring-white/20 transition-all duration-300"
                    placeholder="music, sports, reading, coding"
                    value={step2Data.interests}
                    onChange={(e) => setStep2Data({ ...step2Data, interests: e.target.value })}
                  />
                </motion.div>

                <motion.div
                  className="flex space-x-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 }}
                >
                  <button
                    type="button"
                    onClick={() => setStep(0)}
                    className="flex-1 px-4 py-3 border border-neutral-800 rounded-lg font-medium hover:border-neutral-700 transition-all duration-300 hover:bg-neutral-900/50"
                  >
                    Back
                  </button>
                  <motion.button
                    type="submit"
                    disabled={loading}
                    className="flex-1 px-4 py-3 bg-gradient-to-r from-white to-neutral-200 text-black rounded-lg font-medium hover:from-neutral-200 hover:to-neutral-300 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                    whileHover={{ scale: loading ? 1 : 1.02 }}
                    whileTap={{ scale: loading ? 1 : 0.98 }}
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <motion.span
                          className="w-4 h-4 border-2 border-black border-t-transparent rounded-full mr-2"
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        />
                        Completing...
                      </span>
                    ) : (
                      'Complete Registration'
                    )}
                  </motion.button>
                </motion.div>
              </form>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
