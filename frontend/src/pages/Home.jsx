import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-blue-900/20 to-pink-900/20 animate-pulse"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(120,119,198,0.15),transparent_50%)]"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(219,39,119,0.15),transparent_50%)]"></div>
      
      {/* Navigation */}
      <motion.nav 
        className="border-b border-neutral-800 relative z-10"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-6 sm:px-8">
          <div className="flex items-center justify-between h-16">
            <motion.div 
              className="flex items-center"
              whileHover={{ scale: 1.05 }}
            >
              <h1 className="text-xl font-semibold bg-gradient-to-r from-white to-neutral-400 bg-clip-text text-transparent">
                University Dating
              </h1>
            </motion.div>
            <div className="flex items-center space-x-4">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  to="/login"
                  className="text-sm text-neutral-400 hover:text-white transition-colors duration-300"
                >
                  Sign in
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-gradient-to-r from-white to-neutral-200 text-black rounded-md text-sm font-medium hover:from-neutral-200 hover:to-neutral-300 transition-all duration-300 shadow-lg hover:shadow-xl"
                >
                  Get started
                </Link>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 sm:px-8 pt-20 pb-32 relative z-10">
        <div className="text-center max-w-3xl mx-auto">
          <motion.h1 
            className="text-6xl sm:text-7xl font-bold mb-6 tracking-tight"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          >
            Connect with students
            <motion.span 
              className="block text-transparent bg-clip-text bg-gradient-to-r from-neutral-400 via-neutral-300 to-neutral-500 mt-2"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            >
              from your university
            </motion.span>
          </motion.h1>
          
          <motion.p 
            className="text-xl text-neutral-400 mb-12 leading-relaxed"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
          >
            A safe, exclusive dating platform for university students. 
            Verified .edu emails only. Find meaningful connections on campus.
          </motion.p>
          
          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
          >
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                to="/register"
                className="px-8 py-4 bg-gradient-to-r from-white to-neutral-200 text-black rounded-md font-medium hover:from-neutral-200 hover:to-neutral-300 transition-all duration-300 shadow-lg hover:shadow-xl inline-block"
              >
                Get started
              </Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link
                to="/login"
                className="px-8 py-4 border-2 border-neutral-800 rounded-md font-medium hover:border-neutral-700 hover:bg-neutral-900/50 transition-all duration-300 inline-block"
              >
                Sign in
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Features Section */}
      <div className="border-t border-neutral-800 bg-gradient-to-b from-transparent via-neutral-950/50 to-black relative z-10">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-24">
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-3 gap-12"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            {[
              {
                icon: '🛡️',
                title: 'Verified Students Only',
                description: 'Only students with verified .edu email addresses can join. Your safety is our priority.'
              },
              {
                icon: '💫',
                title: 'Smart Matching',
                description: 'AI-powered matching based on shared interests, school, and compatibility. Find your perfect match.'
              },
              {
                icon: '🎉',
                title: 'Campus Events',
                description: 'Discover and join campus events. Meet people in person at social gatherings and activities.'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="text-center group"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <motion.div 
                  className="w-16 h-16 bg-gradient-to-br from-neutral-800 to-neutral-900 rounded-xl mx-auto mb-4 flex items-center justify-center text-3xl group-hover:from-neutral-700 group-hover:to-neutral-800 transition-all duration-300 shadow-lg"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                >
                  {feature.icon}
                </motion.div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-neutral-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-neutral-800 bg-black relative z-10">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-12">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-neutral-400 text-sm">
              © 2024 University Dating. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              {['Privacy', 'Terms', 'Support'].map((item) => (
                <motion.a
                  key={item}
                  href="#"
                  className="text-neutral-400 hover:text-white text-sm transition-colors duration-300"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {item}
                </motion.a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
