
import { useState } from 'react'
import './App.css'

const initialForm = {
  destination: '',
  start_date: '',
  end_date: '',
  budget: 10000,
  travelers: 1,
  interests: ['food', 'history', 'sightseeing'],
  travel_style: 'balanced',
}

const interestOptions = [
  'food',
  'history',
  'sightseeing',
  'nature',
  'adventure',
  'shopping',
  'culture',
  'relaxation',
]

function App() {
  const [form, setForm] = useState(initialForm)
  const [itinerary, setItinerary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function updateField(event) {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
  }

  function toggleInterest(interest) {
    setForm((previous) => ({
      ...previous,
      interests: previous.interests.includes(interest)
        ? previous.interests.filter((item) => item !== interest)
        : [...previous.interests, interest],
    }))
  }

  async function generateItinerary(event) {
    event.preventDefault()
    setError('')
    setItinerary(null)

    if (form.interests.length === 0) {
      setError('Please select at least one interest.')
      return
    }

    if (form.end_date < form.start_date) {
      setError('Your return date must be on or after your start date.')
      return
    }

    setLoading(true)

    try {
      
const response = await fetch('https://wayfarer-travel-api.onrender.com/api/trips/generate', {

        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          budget: Number(form.budget),
          travelers: Number(form.travelers),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to generate your itinerary.')
      }

      setItinerary(data.itinerary)
    } catch (err) {
      setError(
        err.message.includes('Failed to fetch')
          ? 'Could not connect to the backend. Check that FastAPI is running and CORS is configured.'
          : err.message,
      )
    } finally {
      setLoading(false)
    }
  }

  function resetPlanner() {
    setForm(initialForm)
    setItinerary(null)
    setError('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#home" aria-label="Wayfarer home">
          <span className="brand-icon">✳</span>
          <span>wayfarer<span className="brand-dot">.</span></span>
        </a>
        <nav className="top-nav">
          <a href="#planner">Plan a trip</a>
          <a href="#how-it-works">How it works</a>
        </nav>
        <a className="nav-cta" href="#planner">Start exploring ↗</a>
      </header>

      <main id="home">
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow"><span /> YOUR NEXT ADVENTURE STARTS HERE</div>
            <h1>Less planning.<br />More <em>wonder.</em></h1>
            <p className="hero-description">
              Your own AI travel companion, crafting thoughtful itineraries
              around the places you dream of, your pace, and your budget.
            </p>
            <a className="primary-link" href="#planner">
              Plan my getaway <span>↗</span>
            </a>
            <div className="hero-note">
              <span className="note-stars">✳ ✳ ✳</span>
              Made for curious travellers
            </div>
          </div>
          <div className="hero-art" role="img" aria-label="Travel inspiration">
            <img
              src="https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1100&q=85"
              alt="Warm terracotta buildings and beautiful architecture in Jaipur"
            />
            <div className="image-label">
              <span className="image-label-icon">✦</span>
              <div>
                <strong>Your kind of journey</strong>
                <small>Thoughtfully made for you</small>
              </div>
            </div>
            <div className="floating-stamp">GO<br />EXPLORE<br /><span>↗</span></div>
          </div>
        </section>

        <section className="planner-section" id="planner">
          <div className="section-heading">
            <div>
              <div className="eyebrow">THE ART OF GETTING AWAY</div>
              <h2>Where to <em>next?</em></h2>
              <p>Tell us a little about your trip. We'll take it from there.</p>
            </div>
            <span className="section-number">01 — YOUR TRIP</span>
          </div>

          <form className="planner-form" onSubmit={generateItinerary}>
            <div className="form-grid">
              <label className="field destination-field">
                <span>DESTINATION</span>
                <input
                  name="destination"
                  value={form.destination}
                  onChange={updateField}
                  placeholder="Where would you love to go?"
                  minLength={2}
                  maxLength={100}
                  required
                />
              </label>

              <label className="field">
                <span>DEPARTURE</span>
                <input
                  type="date"
                  name="start_date"
                  value={form.start_date}
                  onChange={updateField}
                  required
                />
              </label>

              <label className="field">
                <span>RETURN</span>
                <input
                  type="date"
                  name="end_date"
                  value={form.end_date}
                  min={form.start_date || undefined}
                  onChange={updateField}
                  required
                />
              </label>

              <label className="field">
                <span>TOTAL BUDGET (₹)</span>
                <input
                  type="number"
                  name="budget"
                  value={form.budget}
                  onChange={updateField}
                  min="1"
                  required
                />
              </label>

              <label className="field">
                <span>TRAVELLERS</span>
                <input
                  type="number"
                  name="travelers"
                  value={form.travelers}
                  onChange={updateField}
                  min="1"
                  max="50"
                  required
                />
              </label>
            </div>

            <div className="interest-area">
              <div className="field-heading">
                <span>WHAT ARE YOU IN THE MOOD FOR?</span>
                <small>Choose all that sound like you</small>
              </div>
              <div className="interest-list">
                {interestOptions.map((interest) => (
                  <button
                    type="button"
                    key={interest}
                    className={`interest-chip ${
                      form.interests.includes(interest) ? 'selected' : ''
                    }`}
                    aria-pressed={form.interests.includes(interest)}
                    onClick={() => toggleInterest(interest)}
                  >
                    <span>{form.interests.includes(interest) ? '✓' : '+'}</span>
                    {interest.charAt(0).toUpperCase() + interest.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-bottom">
              <label className="field style-field">
                <span>YOUR TRAVEL STYLE</span>
                <select
                  name="travel_style"
                  value={form.travel_style}
                  onChange={updateField}
                >
                  <option value="relaxed">Slow & relaxed</option>
                  <option value="balanced">A little of everything</option>
                  <option value="adventure">Adventure seeker</option>
                  <option value="budget">Budget conscious</option>
                  <option value="luxury">Comfort & luxury</option>
                </select>
              </label>
              <button className="generate-button" type="submit" disabled={loading}>
                {loading ? 'Dreaming up your trip…' : 'Create my itinerary ↗'}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message" role="alert">
              <strong>Something needs attention</strong>
              <p>{error}</p>
            </div>
          )}
        </section>

        {loading && (
          <section className="loading-panel" aria-live="polite">
            <div className="loading-icon">✳</div>
            <h2>Gathering a little <em>wanderlust…</em></h2>
            <p>Your AI travel companion is putting your journey together.</p>
          </section>
        )}

        {itinerary && !loading && (
          <section className="results-section" aria-live="polite">
            <div className="results-heading">
              <div>
                <div className="eyebrow">YOUR PERSONALIZED JOURNEY</div>
                <h2>A little trip to <em>{itinerary.destination}</em></h2>
                <p>{itinerary.duration_days} days, thoughtfully planned for you.</p>
              </div>
              <button className="secondary-button" onClick={resetPlanner}>
                + New trip
              </button>
            </div>

            <div className="trip-summary">
              <div><span>DESTINATION</span><strong>{itinerary.destination}</strong></div>
              <div><span>DURATION</span><strong>{itinerary.duration_days} days</strong></div>
              <div><span>ESTIMATED TOTAL</span><strong>₹{Number(itinerary.budget_summary?.estimated_total || 0).toLocaleString('en-IN')}</strong></div>
            </div>

            <div className="days-list">
              {(itinerary.days || []).map((day) => (
                <article className="day-card" key={`${day.day}-${day.date}`}>
                  <div className="day-heading">
                    <div className="day-index">{String(day.day).padStart(2, '0')}</div>
                    <div>
                      <span className="day-kicker">DAY {day.day}</span>
                      <h3>
                        {new Date(`${day.date}T12:00:00`).toLocaleDateString(
                          'en-IN',
                          { weekday: 'long', day: 'numeric', month: 'long' },
                        )}
                      </h3>
                    </div>
                  </div>

                  <div className="activities-grid">
                    {[
                      ['Morning', '☀', day.morning],
                      ['Afternoon', '◒', day.afternoon],
                      ['Evening', '☾', day.evening],
                    ].map(([period, symbol, activity]) => (
                      <div className="activity-card" key={period}>
                        <div className="activity-period">{symbol} {period}</div>
                        <h4>{activity?.activity || 'Explore at your own pace'}</h4>
                        <p>{activity?.description || ''}</p>
                        <div className="activity-cost">
                          Est. ₹{Number(activity?.estimated_cost || 0).toLocaleString('en-IN')}
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="day-extras">
                    <div>
                      <span className="extra-icon">♨</span>
                      <div>
                        <strong>Something delicious</strong>
                        <ul>
                          {(day.food_suggestions || []).map((food, index) => (
                            <li key={`${food}-${index}`}>{food}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    <div>
                      <span className="extra-icon">↗</span>
                      <div>
                        <strong>Getting around</strong>
                        <p>{day.transport_advice}</p>
                      </div>
                    </div>
                  </div>
                </article>
              ))}
            </div>

            <div className="budget-panel">
              <div className="eyebrow">THE MONEY SIDE OF THINGS</div>
              <h3>Your budget, at a glance</h3>
              <p>{itinerary.budget_summary?.notes}</p>
              <div className="budget-total">
                <span>Estimated trip total</span>
                <strong>₹{Number(itinerary.budget_summary?.estimated_total || 0).toLocaleString('en-IN')}</strong>
              </div>
              <small>AI-generated estimates only. Verify actual prices before booking.</small>
            </div>

            <div className="tips-panel">
              <div className="eyebrow">A FEW THINGS TO REMEMBER</div>
              <h3>Little tips for a lovely trip</h3>
              <ul>
                {(itinerary.travel_tips || []).map((tip, index) => (
                  <li key={`${tip}-${index}`}>{tip}</li>
                ))}
              </ul>
            </div>
          </section>
        )}

        <section className="how-section" id="how-it-works">
          <div className="eyebrow">TRAVEL, MADE PERSONAL</div>
          <h2>Three little steps.<br /><em>One lovely journey.</em></h2>
          <div className="steps-grid">
            <article><span>01</span><h3>Tell us your dream</h3><p>Pick a place, your dates, budget and the things you love.</p></article>
            <article><span>02</span><h3>Let AI do its thing</h3><p>Get a personalized itinerary built around your preferences.</p></article>
            <article><span>03</span><h3>Go make memories</h3><p>Explore a day-by-day plan and get ready for your next adventure.</p></article>
          </div>
        </section>
      </main>

      <footer className="footer">
        <a className="brand" href="#home"><span className="brand-icon">✳</span><span>wayfarer<span className="brand-dot">.</span></span></a>
        <p>Thoughtful trips for curious souls.</p>
        <span>AI-generated travel suggestions · Verify details before travelling.</span>
      </footer>
    </div>
  )
}

export default App
