import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Compass,
  ArrowRight,
  ArrowLeft,
  Calendar,
  Users,
  Wallet,
  Sparkles,
  Plane,
  Hotel,
  Check,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import { tripService } from '../services/tripService';
import { useAuth } from '../context/AuthContext';

export const TripWizardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  // Wizard state
  const [step, setStep] = useState<number>(1);
  const [origin, setOrigin] = useState<string>('Mumbai');
  const [destination, setDestination] = useState<string>('Goa');
  const [startDate, setStartDate] = useState<string>('2026-11-15');
  const [endDate, setEndDate] = useState<string>('2026-11-18');
  const [travellers, setTravellers] = useState<number>(2);
  const [budget, setBudget] = useState<number>(45000);
  const [currency, setCurrency] = useState<string>(user?.preferred_currency || 'INR');
  const [travelStyle, setTravelStyle] = useState<string>('Balanced');
  const [interests, setInterests] = useState<string[]>(['Culture', 'Food', 'Sightseeing']);
  const [accommodationPref, setAccommodationPref] = useState<string>('Hotel');
  const [transportPref, setTransportPref] = useState<string>('Best Value');

  // Planning state
  const [isPlanning, setIsPlanning] = useState<boolean>(false);
  const [planningStage, setPlanningStage] = useState<string>('Initializing LangGraph State...');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const availableInterests = [
    'Culture',
    'Food',
    'Sightseeing',
    'Nature',
    'Adventure',
    'Relaxation',
    'Shopping',
    'Nightlife',
  ];

  const travelStyles = [
    { title: 'Budget', desc: 'Hostels, local transit & affordable dining' },
    { title: 'Balanced', desc: 'Boutique stays, mixed transit & top sights' },
    { title: 'Luxury', desc: '5-star resorts, private cabs & fine dining' },
    { title: 'Relaxed', desc: 'Slow travel with fewer daily stops' },
  ];

  const toggleInterest = (item: string) => {
    setInterests((prev) =>
      prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]
    );
  };

  const handleNext = () => {
    if (step === 1) {
      if (!origin.trim() || !destination.trim()) {
        setErrorMsg('Please specify both departure origin and destination.');
        return;
      }
    } else if (step === 2) {
      if (!startDate || !endDate) {
        setErrorMsg('Please select valid departure and return dates.');
        return;
      }
      if (new Date(endDate) < new Date(startDate)) {
        setErrorMsg('Return date cannot be earlier than departure date.');
        return;
      }
    } else if (step === 3) {
      if (budget <= 0) {
        setErrorMsg('Please specify a positive budget.');
        return;
      }
    }
    setErrorMsg(null);
    setStep((s) => s + 1);
  };

  const handleBack = () => {
    setErrorMsg(null);
    setStep((s) => s - 1);
  };

  const handleSubmit = async () => {
    setIsPlanning(true);
    setErrorMsg(null);

    // Simulate agent steps in UI while API executes the real LangGraph workflow
    const stages = [
      'Validating traveler constraints and dates...',
      'Retrieving verified geographic coordinates and attraction catalog...',
      'Transportation Agent: Benchmarking flight, train, bus and road routes...',
      'Hotel Agent: Discovering and ranking accommodations...',
      'Weather Intelligence Agent: Querying meteorological forecasts...',
      'Trip Planner Agent: Sequencing chronological daily schedule...',
      'Budget Optimization Agent: Reconciling deterministic totals and contingency...',
      'Safety Agent: Performing schedule feasibility and advisory checks...',
      'Assembling final verified trip plan...',
    ];

    let stageIdx = 0;
    const interval = setInterval(() => {
      if (stageIdx < stages.length - 1) {
        stageIdx += 1;
        setPlanningStage(stages[stageIdx]);
      }
    }, 900);

    try {
      const trip = await tripService.createTrip({
        origin,
        destination,
        start_date: startDate,
        end_date: endDate,
        travellers,
        total_budget: budget,
        currency,
        travel_style: travelStyle,
        interests,
        accommodation_pref: accommodationPref,
        transport_pref: transportPref,
      });

      clearInterval(interval);
      navigate(`/trips/${trip.id}`);
    } catch (err: any) {
      clearInterval(interval);
      console.error('Trip generation failed:', err);
      setIsPlanning(false);
      setErrorMsg(
        err.response?.data?.detail ||
          'Failed to orchestrate trip workflow. Please review your inputs and try again.'
      );
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12 text-left">
      {/* Wizard Progress Stepper */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-3 text-xs font-bold text-[#143628]">
          <span>Step {step} of 4</span>
          <span>
            {step === 1 && 'Destination & Origin'}
            {step === 2 && 'Dates & Travellers'}
            {step === 3 && 'Budget & Style'}
            {step === 4 && 'Preferences & Confirmation'}
          </span>
        </div>
        <div className="w-full bg-[#E7E5DF] h-2 rounded-full overflow-hidden">
          <div
            className="bg-[#10B981] h-full transition-all duration-300"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>
      </div>

      {/* Main Form Card */}
      <div className="bg-white rounded-3xl border border-[#E7E5DF] shadow-xl p-8 sm:p-10 space-y-8">
        {errorMsg && (
          <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-xs rounded-2xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* STEP 1: Destination & Origin */}
        {step === 1 && (
          <div className="space-y-6 animate-fade-in">
            <div>
              <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
                Stage 1 &bull; Routing
              </span>
              <h2 className="font-editorial text-2xl sm:text-3xl font-bold text-[#0F1E28] mt-1">
                Where are you setting out from and heading to?
              </h2>
              <p className="text-xs text-[#5A6D7C] mt-1">
                Enter your starting city and destination. Our agents will look up verified attractions and transit routes.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Origin City
                </label>
                <input
                  type="text"
                  required
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  placeholder="e.g. Mumbai, Delhi, Paris"
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] text-sm text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Destination
                </label>
                <input
                  type="text"
                  required
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  placeholder="e.g. Goa, Jaipur, Tokyo, Paris"
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] text-sm text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                />
              </div>
            </div>

            {/* Quick destination suggestion buttons */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-semibold text-[#8C9BA5]">
                  Popular Verified Locations:
                </span>
                <span className="text-[11px] font-bold text-[#059669]">
                  38 Tamil Nadu Districts Added
                </span>
              </div>

              <div className="flex flex-wrap gap-2 mb-3">
                {['Chennai', 'Madurai', 'Ooty', 'Kodaikanal', 'Rameswaram', 'Kanyakumari', 'Thanjavur', 'Coimbatore', 'Goa', 'Jaipur'].map((city) => (
                  <button
                    key={city}
                    type="button"
                    onClick={() => setDestination(city)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                      destination.toLowerCase() === city.toLowerCase()
                        ? 'bg-[#143628] text-white border-[#143628]'
                        : 'bg-[#FAF9F5] text-[#2C3E50] border-[#E7E5DF] hover:border-[#10B981]'
                    }`}
                  >
                    {city}
                  </button>
                ))}
              </div>

              {/* Dedicated All 38 Tamil Nadu Districts Selector */}
              <div className="p-3 bg-[#F0FDF4] border border-[#BBF7D0] rounded-xl text-left">
                <label className="text-[11px] font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Select Any Tamil Nadu District (All 38 Curated with GPS & Landmarks):
                </label>
                <select
                  value={destination}
                  onChange={(e) => {
                    if (e.target.value) setDestination(e.target.value);
                  }}
                  className="w-full px-3 py-2 text-xs bg-white border border-[#86EFAC] rounded-lg text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                >
                  <option value="">-- Choose from all 38 Tamil Nadu Districts --</option>
                  <option value="Ariyalur">Ariyalur (Gangaikonda Cholapuram & Dinosaur Fossils)</option>
                  <option value="Chengalpattu">Chengalpattu (Mahabalipuram & Shore Temple)</option>
                  <option value="Chennai">Chennai (Marina Beach & Mylapore Kapaleeshwarar)</option>
                  <option value="Coimbatore">Coimbatore (Isha Adiyogi & Marudhamalai)</option>
                  <option value="Cuddalore">Cuddalore (Pichavaram Mangrove Forests)</option>
                  <option value="Dharmapuri">Dharmapuri (Hogenakkal Waterfalls)</option>
                  <option value="Dindigul">Dindigul (Kodaikanal Hill Station & Lake)</option>
                  <option value="Erode">Erode (Bhavani Sangameshwarar & Kodiveri Dam)</option>
                  <option value="Kallakurichi">Kallakurichi (Kalrayan Hills & Megam Falls)</option>
                  <option value="Kanchipuram">Kanchipuram (Kailasanathar & Silk Weaving)</option>
                  <option value="Kanyakumari">Kanyakumari (Vivekananda Rock & Sunset Point)</option>
                  <option value="Karur">Karur (Pasupatheeswarar & Mayanur Barrage)</option>
                  <option value="Krishnagiri">Krishnagiri (Krishnagiri Dam & Sayed Basha Fort)</option>
                  <option value="Madurai">Madurai (Meenakshi Amman & Thirumalai Nayakkar)</option>
                  <option value="Mayiladuthurai">Mayiladuthurai (Tranquebar Dutch Fort & Poompuhar)</option>
                  <option value="Nagapattinam">Nagapattinam (Velankanni Basilica & Soundararaja)</option>
                  <option value="Namakkal">Namakkal (Kolli Hills 70 Hairpin Bends & Agaya Gangai)</option>
                  <option value="Nilgiris">Nilgiris (Ooty Botanical Garden & Toy Train)</option>
                  <option value="Perambalur">Perambalur (Ranjankudi Fortress & Siruvachur)</option>
                  <option value="Pudukkottai">Pudukkottai (Sittanavasal Caves & Thirumayam Fort)</option>
                  <option value="Ramanathapuram">Ramanathapuram (Rameswaram Temple & Dhanushkodi)</option>
                  <option value="Ranipet">Ranipet (Arcot Fortress & Mahendravadi Caves)</option>
                  <option value="Salem">Salem (Yercaud Hill Station & Mettur Dam)</option>
                  <option value="Sivagangai">Sivagangai (Chettinad Mansions & Kanadukathan)</option>
                  <option value="Tenkasi">Tenkasi (Courtallam Waterfalls & Kasi Viswanathar)</option>
                  <option value="Thanjavur">Thanjavur (Brihadisvara Big Temple & Palace)</option>
                  <option value="Theni">Theni (Megamalai Cloud Mountain & Suruli Falls)</option>
                  <option value="Thoothukudi">Thoothukudi (Tiruchendur Murugan & Hare Island)</option>
                  <option value="Tiruchirappalli">Tiruchirappalli (Srirangam Temple & Rockfort)</option>
                  <option value="Tirunelveli">Tirunelveli (Nellaiappar Temple & Manimuthar)</option>
                  <option value="Tirupathur">Tirupathur (Yelagiri Hills & Jalagamparai)</option>
                  <option value="Tiruppur">Tiruppur (Uthukuli & Amaravathi Crocodile Bank)</option>
                  <option value="Tiruvallur">Tiruvallur (Pulicat Lake Bird Sanctuary & Poondi)</option>
                  <option value="Tiruvannamalai">Tiruvannamalai (Annamalaiyar Temple & Giri Valam)</option>
                  <option value="Tiruvarur">Tiruvarur (Thyagaraja Chariot & Muthupet Mangroves)</option>
                  <option value="Vellore">Vellore (Vellore Fort & Sripuram Golden Temple)</option>
                  <option value="Viluppuram">Viluppuram (Gingee Fort - Troy of the East)</option>
                  <option value="Virudhunagar">Virudhunagar (Srivilliputhur Andal Tower & Shenbagathoppu)</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: Dates & Travellers */}
        {step === 2 && (
          <div className="space-y-6 animate-fade-in">
            <div>
              <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
                Stage 2 &bull; Timeframe & Party
              </span>
              <h2 className="font-editorial text-2xl sm:text-3xl font-bold text-[#0F1E28] mt-1">
                When are you travelling and with whom?
              </h2>
              <p className="text-xs text-[#5A6D7C] mt-1">
                Dates are passed to the Weather Agent to pull real-time forecasts or seasonal models.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Departure Date
                </label>
                <input
                  type="date"
                  required
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] text-sm text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Return Date
                </label>
                <input
                  type="date"
                  required
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] text-sm text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                Number of Travellers
              </label>
              <div className="flex items-center gap-3">
                <Users className="w-5 h-5 text-[#10B981]" />
                <input
                  type="number"
                  min={1}
                  max={30}
                  value={travellers}
                  onChange={(e) => setTravellers(Number(e.target.value))}
                  className="w-32 px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-sm font-bold text-[#0F1E28]"
                />
                <span className="text-xs text-[#5A6D7C]">
                  Accommodation rooms and per-person dining scaled automatically.
                </span>
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: Budget & Travel Style */}
        {step === 3 && (
          <div className="space-y-6 animate-fade-in">
            <div>
              <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
                Stage 3 &bull; Financial & Style Bounds
              </span>
              <h2 className="font-editorial text-2xl sm:text-3xl font-bold text-[#0F1E28] mt-1">
                Set your budget ceiling and preferred travel pace
              </h2>
              <p className="text-xs text-[#5A6D7C] mt-1">
                The Budget Agent will mathematically reconcile all category expenses and guarantee 5% contingency.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="sm:col-span-2">
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Total Budget Limit
                </label>
                <div className="relative">
                  <Wallet className="w-4 h-4 text-[#8C9BA5] absolute left-3.5 top-3.5" />
                  <input
                    type="number"
                    min={1000}
                    step={1000}
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-[#CBD5E1] text-sm font-bold text-[#0F1E28] focus:ring-2 focus:ring-[#10B981] focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Currency
                </label>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-[#CBD5E1] text-sm font-semibold text-[#0F1E28] bg-white focus:ring-2 focus:ring-[#10B981]"
                >
                  <option value="INR">INR (₹)</option>
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="GBP">GBP (£)</option>
                </select>
              </div>
            </div>

            {/* Travel Style Selector */}
            <div>
              <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-2">
                Travel Style & Pace
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {travelStyles.map((style) => (
                  <div
                    key={style.title}
                    onClick={() => setTravelStyle(style.title)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all ${
                      travelStyle === style.title
                        ? 'border-[#10B981] bg-[#10B981]/10 shadow-sm'
                        : 'border-[#E7E5DF] bg-[#FAF9F5] hover:border-[#CBD5E1]'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-sm text-[#0F1E28]">{style.title}</span>
                      {travelStyle === style.title && (
                        <Check className="w-4 h-4 text-[#10B981]" />
                      )}
                    </div>
                    <p className="text-xs text-[#5A6D7C]">{style.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* STEP 4: Interests & Final Confirmation */}
        {step === 4 && (
          <div className="space-y-6 animate-fade-in">
            <div>
              <span className="text-xs font-bold text-[#059669] uppercase tracking-wider">
                Stage 4 &bull; Interests & Transport Preference
              </span>
              <h2 className="font-editorial text-2xl sm:text-3xl font-bold text-[#0F1E28] mt-1">
                What interests you most?
              </h2>
              <p className="text-xs text-[#5A6D7C] mt-1">
                The Planner Agent will prioritize activities that reflect your chosen topics.
              </p>
            </div>

            {/* Interests Chips */}
            <div>
              <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-2">
                Select Your Interests
              </label>
              <div className="flex flex-wrap gap-2">
                {availableInterests.map((item) => (
                  <button
                    key={item}
                    type="button"
                    onClick={() => toggleInterest(item)}
                    className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-all ${
                      interests.includes(item)
                        ? 'bg-[#143628] text-white border-[#143628] shadow-sm'
                        : 'bg-[#FAF9F5] text-[#2C3E50] border-[#E7E5DF] hover:border-[#CBD5E1]'
                    }`}
                  >
                    {interests.includes(item) && '✓ '} {item}
                  </button>
                ))}
              </div>
            </div>

            {/* Mode & Lodging Preferences */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Accommodation Preference
                </label>
                <select
                  value={accommodationPref}
                  onChange={(e) => setAccommodationPref(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs font-semibold text-[#0F1E28] bg-white"
                >
                  <option value="Hotel">Standard Hotel (3-Star+)</option>
                  <option value="Boutique">Heritage Boutique Hotel</option>
                  <option value="Resort">Luxury Resort & Spa</option>
                  <option value="Hostel">Budget Social Hostel</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-[#143628] uppercase tracking-wider block mb-1">
                  Transit Preference
                </label>
                <select
                  value={transportPref}
                  onChange={(e) => setTransportPref(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-[#CBD5E1] text-xs font-semibold text-[#0F1E28] bg-white"
                >
                  <option value="Best Value">Best Value (Balanced)</option>
                  <option value="Flight">Flight (Fastest)</option>
                  <option value="Train">Express Train (Scenic Rail)</option>
                  <option value="Bus">Overnight Bus / Coach</option>
                  <option value="Cab">Private Outstation Cab</option>
                </select>
              </div>
            </div>

            {/* Summary Review Card */}
            <div className="p-4 rounded-2xl bg-[#FAF9F5] border border-[#E7E5DF] text-xs space-y-1">
              <span className="font-bold text-[#0F1E28] uppercase tracking-wider text-[10px] block text-[#059669]">
                Session Parameters Preview:
              </span>
              <p className="text-[#2C3E50]">
                <strong>{origin}</strong> &rarr; <strong>{destination}</strong> &bull; {startDate} to {endDate} &bull; {travellers} traveller(s)
              </p>
              <p className="text-[#2C3E50]">
                Budget: <strong>{currency} {budget.toLocaleString()}</strong> &bull; Style: <strong>{travelStyle}</strong> &bull; Interests: {interests.join(', ')}
              </p>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        {!isPlanning && (
          <div className="pt-4 border-t border-[#F1F0EB] flex items-center justify-between">
            {step > 1 ? (
              <button
                type="button"
                onClick={handleBack}
                className="px-5 py-2.5 rounded-xl border border-[#CBD5E1] text-xs font-semibold text-[#5A6D7C] hover:bg-black/5 flex items-center gap-1.5"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
            ) : (
              <div />
            )}

            {step < 4 ? (
              <button
                type="button"
                onClick={handleNext}
                className="px-6 py-2.5 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white text-xs font-bold flex items-center gap-2 shadow-md transition-all"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4 text-[#10B981]" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                className="px-8 py-3 rounded-xl bg-gradient-to-r from-[#143628] to-[#10B981] hover:from-[#1E4D3B] hover:to-[#059669] text-white text-xs font-bold flex items-center gap-2.5 shadow-lg shadow-[#10B981]/25 transition-all hover:scale-105"
              >
                <Sparkles className="w-4 h-4 text-emerald-200" />
                <span>Launch Multi-Agent Orchestration</span>
              </button>
            )}
          </div>
        )}

        {/* Real-time Multi-Agent Planning Overlay */}
        {isPlanning && (
          <div className="py-8 text-center space-y-6 animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-[#143628] text-[#10B981] flex items-center justify-center mx-auto shadow-xl">
              <RefreshCw className="w-8 h-8 animate-spin" />
            </div>

            <div className="space-y-2 max-w-md mx-auto">
              <h3 className="font-editorial text-2xl font-bold text-[#0F1E28]">
                Multi-Agent Swarm in Execution
              </h3>
              <p className="text-xs text-[#059669] font-semibold flex items-center justify-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[#10B981] animate-ping" />
                {planningStage}
              </p>
              <p className="text-[11px] text-[#5A6D7C] leading-relaxed pt-2">
                Agents are executing collaborative decision-making across LangGraph. Computing haversine distances, fetching Open-Meteo forecasts, and reconciling financial math...
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
