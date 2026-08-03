export default function Navbar() {
  const scrollTo = (id) => {
    document.getElementById(id).scrollIntoView({ behavior: "smooth" })
  }

  return (
    <nav className="w-full bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
      <span className="text-lg font-bold text-gray-900">Elevora</span>
      <div className="flex gap-6">
        <button
          onClick={() => scrollTo('about')}
          className="text-sm text-gray-600 hover:text-blue-600 transition"
        >
          About
        </button>
        <button
          onClick={() => scrollTo('help')}
          className="text-sm text-gray-600 hover:text-blue-600 transition"
        >
          Help Center
        </button>
      </div>
    </nav>
  )
}
