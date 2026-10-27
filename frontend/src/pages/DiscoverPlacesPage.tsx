import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  MapPin, 
  Clock, 
  Tag, 
  ExternalLink, 
  Compass, 
  Sparkles, 
  Filter, 
  X, 
  Calendar, 
  Info, 
  Navigation, 
  CheckCircle2, 
  Accessibility,
  ArrowRight
} from 'lucide-react';
import { placesService, PlaceItem, CategoryCount, AreaZoneCount } from '../services/placesService';

export const DiscoverPlacesPage: React.FC = () => {
  const navigate = useNavigate();

  // State
  const [places, setPlaces] = useState<PlaceItem[]>([]);
  const [categories, setCategories] = useState<CategoryCount[]>([]);
  const [zones, setZones] = useState<AreaZoneCount[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isLoadingMore, setIsLoadingMore] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Filters & Pagination
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedZone, setSelectedZone] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('default');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(false);

  // Modal State
  const [activeModalPlace, setActiveModalPlace] = useState<PlaceItem | null>(null);

  // Initial Fetch & Filter Fetch
  const fetchPlaces = async (page: number, append: boolean = false) => {
    try {
      if (append) {
        setIsLoadingMore(true);
      } else {
        setIsLoading(true);
      }
      setError(null);

      const res = await placesService.searchPlaces({
        query: searchQuery.trim() || undefined,
        category: selectedCategory !== 'all' ? selectedCategory : undefined,
        area_zone: selectedZone !== 'all' ? selectedZone : undefined,
        sort_by: sortBy,
        page,
        limit: 12,
      });

      if (append) {
        setPlaces((prev) => [...prev, ...res.results]);
      } else {
        setPlaces(res.results);
      }

      setTotalCount(res.total);
      setHasMore(res.has_more);
      if (res.available_categories) setCategories(res.available_categories);
      if (res.available_zones) setZones(res.available_zones);
    } catch (err: any) {
      console.error('Failed to load discover places:', err);
      setError('Unable to load verified destinations. Please check your network or backend connection.');
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  };

  // Re-fetch on filter changes
  useEffect(() => {
    setCurrentPage(1);
    fetchPlaces(1, false);
  }, [searchQuery, selectedZone, selectedCategory, sortBy]);

  const handleLoadMore = () => {
    if (!hasMore || isLoadingMore) return;
    const nextPage = currentPage + 1;
    setCurrentPage(nextPage);
    fetchPlaces(nextPage, true);
  };

  const handlePlanTripToPlace = (place: PlaceItem) => {
    navigate('/wizard', {
      state: {
        prefilledDestination: place.city || 'Chennai',
        prefilledInterests: [place.category],
      },
    });
  };

  return (
    <div className="min-h-screen bg-[#FAF9F5] text-[#0F1E28] pb-24">
      {/* Hero Header */}
      <section className="bg-gradient-to-b from-[#143628] to-[#1A4232] text-white pt-12 pb-16 px-4 sm:px-6 lg:px-8 border-b border-emerald-900/30">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="flex flex-wrap items-center gap-2">
            <span className="bg-[#10B981] text-[#143628] text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider shadow-sm flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              Verified Destination Catalog
            </span>
            <span className="text-xs text-emerald-200 font-semibold px-2.5 py-0.5 rounded-full bg-white/10 border border-white/15">
              Chennai & Metropolitan Area
            </span>
            <span className="text-xs text-amber-200 font-bold px-2.5 py-0.5 rounded-full bg-amber-500/20 border border-amber-400/30">
              54+ Verified Spots • Zero 3-Place Limit
            </span>
          </div>

          <div className="max-w-3xl space-y-3">
            <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight font-editorial leading-tight">
              Discover Chennai, Greater Suburbs & Day Trips
            </h1>
            <p className="text-sm sm:text-base text-emerald-100/85 leading-relaxed">
              Explore 54 verified cultural monuments, golden waterfronts, sacred sanctuaries, historic museums, 
              and tranquil nature reserves. Sourced directly from TTDC, Incredible India, and Chennai District Tourism.
            </p>
          </div>

          {/* Area Zone Filter Tabs */}
          <div className="pt-2 flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedZone('all')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-2 ${
                selectedZone === 'all'
                  ? 'bg-[#10B981] text-[#143628] scale-105 shadow-md'
                  : 'bg-white/10 hover:bg-white/20 text-white border border-white/15'
              }`}
            >
              <span>All Locations</span>
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-black/20 font-black">
                {zones.reduce((acc, z) => acc + z.count, 0) || 54}
              </span>
            </button>
            {zones.map((z) => (
              <button
                key={z.zone}
                onClick={() => setSelectedZone(z.zone)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-2 ${
                  selectedZone === z.zone
                    ? 'bg-[#10B981] text-[#143628] scale-105 shadow-md'
                    : 'bg-white/10 hover:bg-white/20 text-white border border-white/15'
                }`}
              >
                <span>{z.label}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-black/20 font-black">
                  {z.count}
                </span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-6">
        {/* Controls Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-[#E7E5DF] p-4 sm:p-6 mb-8 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            {/* Search Input */}
            <div className="md:col-span-6 relative">
              <Search className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8C9BA5]" />
              <input
                type="text"
                placeholder="Search by name, neighborhood (e.g. Mylapore, ECR), or keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-11 pr-10 py-3 bg-[#F8F9FA] border border-[#E2E8F0] rounded-xl text-sm text-[#0F1E28] placeholder-[#8C9BA5] focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8C9BA5] hover:text-[#0F1E28]"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Category Dropdown */}
            <div className="md:col-span-3">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full py-3 px-3.5 bg-[#F8F9FA] border border-[#E2E8F0] rounded-xl text-sm font-medium text-[#0F1E28] focus:outline-none focus:ring-2 focus:ring-[#10B981]"
              >
                <option value="all">All Categories ({categories.reduce((a, b) => a + b.count, 0) || 54})</option>
                {categories.map((c) => (
                  <option key={c.category} value={c.category}>
                    {c.category} ({c.count})
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Dropdown */}
            <div className="md:col-span-3">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full py-3 px-3.5 bg-[#F8F9FA] border border-[#E2E8F0] rounded-xl text-sm font-medium text-[#0F1E28] focus:outline-none focus:ring-2 focus:ring-[#10B981]"
              >
                <option value="default">Sort: Recommended</option>
                <option value="name_asc">Name: A to Z</option>
                <option value="name_desc">Name: Z to A</option>
                <option value="duration_asc">Duration: Shortest First</option>
                <option value="duration_desc">Duration: Longest First</option>
                <option value="price_asc">Ticket: Free / Lowest First</option>
              </select>
            </div>
          </div>

          {/* Quick Category Chips */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs pt-1 no-scrollbar">
            <span className="text-[#8C9BA5] font-semibold text-xs flex items-center gap-1 shrink-0">
              <Filter className="w-3.5 h-3.5" /> Filter:
            </span>
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-3 py-1.5 rounded-lg font-bold shrink-0 transition-colors ${
                selectedCategory === 'all'
                  ? 'bg-[#143628] text-white'
                  : 'bg-[#F1F3F5] text-[#5A6D7C] hover:bg-[#E2E8F0]'
              }`}
            >
              All Categories
            </button>
            {categories.slice(0, 7).map((c) => (
              <button
                key={c.category}
                onClick={() => setSelectedCategory(c.category)}
                className={`px-3 py-1.5 rounded-lg font-semibold shrink-0 transition-colors ${
                  selectedCategory === c.category
                    ? 'bg-[#143628] text-white'
                    : 'bg-[#F1F3F5] text-[#5A6D7C] hover:bg-[#E2E8F0]'
                }`}
              >
                {c.category}
              </button>
            ))}
          </div>
        </div>

        {/* Results Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
          <div className="flex items-center gap-3">
            <h2 className="text-xl sm:text-2xl font-bold font-editorial text-[#0F1E28]">
              {selectedZone === 'all' ? 'All Verified Destinations' : zones.find(z => z.zone === selectedZone)?.label || 'Destinations'}
            </h2>
            <span className="bg-[#10B981]/15 text-[#059669] font-extrabold text-xs px-2.5 py-1 rounded-full border border-[#10B981]/30">
              {totalCount} Verified Places Found
            </span>
          </div>

          <div className="text-xs text-[#5A6D7C] flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
            <span>Showing verified hours, addresses & GPS coordinates</span>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm mb-6 flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={() => fetchPlaces(1)}
              className="px-3 py-1 bg-rose-800 text-white text-xs font-bold rounded-lg hover:bg-rose-900"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 py-12">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div key={n} className="bg-white rounded-2xl p-5 border border-[#E7E5DF] animate-pulse space-y-4">
                <div className="h-44 bg-gray-200 rounded-xl w-full" />
                <div className="h-4 bg-gray-200 rounded w-3/4" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
                <div className="h-10 bg-gray-200 rounded-xl w-full mt-4" />
              </div>
            ))}
          </div>
        )}

        {/* Places Grid */}
        {!isLoading && places.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {places.map((place) => (
              <div
                key={place.id}
                className="bg-white rounded-2xl border border-[#E7E5DF] overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col group"
              >
                {/* Image Banner */}
                <div className="relative h-48 w-full bg-[#143628] overflow-hidden">
                  <img
                    src={place.image_url || 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80'}
                    alt={place.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

                  {/* Badges */}
                  <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
                    <span className="bg-white/95 backdrop-blur-sm text-[#143628] text-[11px] font-black px-2.5 py-0.5 rounded-full shadow-sm">
                      {place.category}
                    </span>
                    {place.area_zone === 'day_trips' ? (
                      <span className="bg-amber-400 text-amber-950 text-[10px] font-black px-2 py-0.5 rounded-full shadow-sm">
                        Day Trip (Outside City)
                      </span>
                    ) : place.area_zone === 'greater_chennai' ? (
                      <span className="bg-emerald-700 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm">
                        Greater Chennai
                      </span>
                    ) : (
                      <span className="bg-[#143628] text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm">
                        City Central
                      </span>
                    )}
                  </div>

                  {/* Price Tag Overlay */}
                  <div className="absolute bottom-3 right-3 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-lg text-white text-xs font-bold border border-white/20">
                    {place.ticket_price_inr === 0 ? 'Free Entry' : `₹${place.ticket_price_inr}`}
                  </div>

                  {/* Locality Overlay */}
                  <div className="absolute bottom-3 left-3 text-white">
                    <p className="text-xs font-semibold flex items-center gap-1 text-emerald-300">
                      <MapPin className="w-3.5 h-3.5" />
                      {place.locality}
                    </p>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div className="space-y-2">
                    <h3 className="font-editorial text-lg font-bold text-[#0F1E28] leading-snug group-hover:text-[#10B981] transition-colors line-clamp-1">
                      {place.name}
                    </h3>
                    <p className="text-xs text-[#5A6D7C] line-clamp-2 leading-relaxed">
                      {place.desc}
                    </p>
                  </div>

                  {/* Metadata Chips */}
                  <div className="pt-2 border-t border-[#F1F3F5] space-y-2 text-xs text-[#5A6D7C]">
                    <div className="flex items-center justify-between">
                      <span className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-[#10B981]" />
                        <span className="truncate max-w-[190px]">{place.opening_hours}</span>
                      </span>
                      <span className="font-semibold text-[#0F1E28] shrink-0">
                        ~{place.visit_duration_hours} hrs
                      </span>
                    </div>

                    {place.closed_days && place.closed_days !== 'None' && (
                      <div className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        Closed: {place.closed_days}
                      </div>
                    )}

                    {place.accessibility_notes && (
                      <div className="text-[11px] text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 flex items-center gap-1">
                        <Accessibility className="w-3 h-3 text-emerald-600 shrink-0" />
                        <span className="truncate">{place.accessibility_notes}</span>
                      </div>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="pt-3 grid grid-cols-2 gap-2">
                    <button
                      onClick={() => setActiveModalPlace(place)}
                      className="w-full py-2.5 px-3 rounded-xl bg-[#F8F9FA] hover:bg-[#E2E8F0] text-[#0F1E28] font-bold text-xs flex items-center justify-center gap-1.5 border border-[#E2E8F0] transition-colors"
                    >
                      <Info className="w-3.5 h-3.5 text-[#143628]" />
                      <span>Details & Map</span>
                    </button>
                    <button
                      onClick={() => handlePlanTripToPlace(place)}
                      className="w-full py-2.5 px-3 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition-colors"
                    >
                      <span>Plan Trip</span>
                      <ArrowRight className="w-3.5 h-3.5 text-[#10B981]" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && places.length === 0 && (
          <div className="bg-white rounded-3xl border border-[#E7E5DF] p-12 text-center max-w-lg mx-auto space-y-4 my-8">
            <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center text-emerald-600 mx-auto">
              <Compass className="w-7 h-7" />
            </div>
            <h3 className="font-editorial text-2xl font-bold text-[#0F1E28]">
              No matching destinations found
            </h3>
            <p className="text-xs sm:text-sm text-[#5A6D7C]">
              We couldn't find any places matching your criteria "{searchQuery}". Try clearing some filters or searching for another neighborhood.
            </p>
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
                setSelectedZone('all');
              }}
              className="px-5 py-2.5 bg-[#143628] text-white font-bold text-xs rounded-xl hover:bg-[#1E4D3B] transition-colors"
            >
              Reset All Filters
            </button>
          </div>
        )}

        {/* Load More Button (Removes pagination limits) */}
        {!isLoading && hasMore && (
          <div className="text-center pt-10">
            <button
              onClick={handleLoadMore}
              disabled={isLoadingMore}
              className="px-8 py-3.5 rounded-2xl bg-[#143628] hover:bg-[#1A4232] text-white font-extrabold text-sm shadow-lg hover:shadow-xl transition-all duration-200 inline-flex items-center gap-2 border border-emerald-500/30"
            >
              {isLoadingMore ? (
                <>
                  <div className="w-4 h-4 border-2 border-[#10B981] border-t-transparent rounded-full animate-spin" />
                  <span>Loading More Places...</span>
                </>
              ) : (
                <>
                  <span>Load More Destinations</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-[#10B981] text-[#143628] font-black">
                    +{totalCount - places.length} remaining
                  </span>
                </>
              )}
            </button>
            <p className="text-xs text-[#8C9BA5] mt-2 font-medium">
              Showing {places.length} of {totalCount} verified Chennai places
            </p>
          </div>
        )}
      </div>

      {/* Place Details Modal */}
      {activeModalPlace && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-[#E7E5DF] relative">
            {/* Close Button */}
            <button
              onClick={() => setActiveModalPlace(null)}
              className="absolute top-4 right-4 z-10 w-9 h-9 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Modal Image Header */}
            <div className="relative h-60 w-full bg-[#143628]">
              <img
                src={activeModalPlace.image_url || 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80'}
                alt={activeModalPlace.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-transparent" />
              <div className="absolute bottom-4 left-6 right-6 text-white space-y-1">
                <div className="flex flex-wrap gap-2">
                  <span className="bg-[#10B981] text-[#143628] text-xs font-black px-2.5 py-0.5 rounded-full">
                    {activeModalPlace.category}
                  </span>
                  <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-0.5 rounded-full">
                    {activeModalPlace.area_label}
                  </span>
                </div>
                <h2 className="text-2xl font-bold font-editorial text-white">
                  {activeModalPlace.name}
                </h2>
                <p className="text-xs text-emerald-200 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5" />
                  {activeModalPlace.locality}, {activeModalPlace.district}
                </p>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6 sm:p-8 space-y-6">
              <div className="space-y-2">
                <h4 className="text-xs font-extrabold uppercase text-[#8C9BA5] tracking-wider">
                  About Destination
                </h4>
                <p className="text-sm text-[#2C3E50] leading-relaxed">
                  {activeModalPlace.desc}
                </p>
              </div>

              {/* Verified Details Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-[#F8F9FA] p-4 rounded-2xl border border-[#E7E5DF] text-xs">
                <div>
                  <span className="text-[#8C9BA5] font-semibold block mb-1">Opening Hours</span>
                  <span className="font-bold text-[#0F1E28]">{activeModalPlace.opening_hours}</span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] font-semibold block mb-1">Weekly Closed Day</span>
                  <span className="font-bold text-[#0F1E28]">{activeModalPlace.closed_days || 'Open Everyday'}</span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] font-semibold block mb-1">Entry Ticket</span>
                  <span className="font-bold text-[#0F1E28]">
                    {activeModalPlace.ticket_price_inr === 0 ? 'Free Public Entry' : `₹${activeModalPlace.ticket_price_inr} per person`}
                  </span>
                </div>
                <div>
                  <span className="text-[#8C9BA5] font-semibold block mb-1">Recommended Duration</span>
                  <span className="font-bold text-[#0F1E28]">{activeModalPlace.visit_duration_hours} hours</span>
                </div>
              </div>

              {/* Full Address & GPS */}
              <div className="space-y-2">
                <span className="text-xs font-extrabold uppercase text-[#8C9BA5] tracking-wider">
                  Full Address & Coordinates
                </span>
                <p className="text-xs text-[#2C3E50] bg-white p-3 rounded-xl border border-[#E7E5DF]">
                  {activeModalPlace.address}
                </p>
                <div className="text-[11px] text-[#8C9BA5] font-mono">
                  GPS: {activeModalPlace.lat.toFixed(4)}° N, {activeModalPlace.lng.toFixed(4)}° E
                </div>
              </div>

              {/* Accessibility */}
              {activeModalPlace.accessibility_notes && (
                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 flex items-start gap-2">
                  <Accessibility className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold block">Accessibility Information:</span>
                    <span>{activeModalPlace.accessibility_notes}</span>
                  </div>
                </div>
              )}

              {/* Source Attribution */}
              <div className="text-[11px] text-[#8C9BA5] border-t border-[#E7E5DF] pt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <span>Verified by: {activeModalPlace.source_attribution}</span>
                <span>Last Verified: {activeModalPlace.last_updated}</span>
              </div>

              {/* Action Buttons in Modal */}
              <div className="pt-2 flex flex-col sm:flex-row gap-3">
                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                    activeModalPlace.name + ', ' + activeModalPlace.address
                  )}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 py-3 px-4 rounded-xl bg-[#10B981] hover:bg-[#059669] text-[#143628] font-extrabold text-xs flex items-center justify-center gap-2 shadow transition-colors"
                >
                  <Navigation className="w-4 h-4" />
                  <span>Open in Google Maps</span>
                  <ExternalLink className="w-3.5 h-3.5 opacity-70" />
                </a>

                {activeModalPlace.official_website && (
                  <a
                    href={activeModalPlace.official_website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="py-3 px-4 rounded-xl bg-[#F1F3F5] hover:bg-[#E2E8F0] text-[#0F1E28] font-bold text-xs flex items-center justify-center gap-2 border border-[#E2E8F0] transition-colors"
                  >
                    <span>Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}

                <button
                  onClick={() => {
                    setActiveModalPlace(null);
                    handlePlanTripToPlace(activeModalPlace);
                  }}
                  className="py-3 px-5 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white font-extrabold text-xs flex items-center justify-center gap-2 shadow transition-colors"
                >
                  <span>Build Itinerary</span>
                  <ArrowRight className="w-4 h-4 text-[#10B981]" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
