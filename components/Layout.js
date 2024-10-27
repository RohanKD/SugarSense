import Link from 'next/link';
import { useRouter } from 'next/router';
import Image from 'next/image';

export default function Layout({ children }) {
  const router = useRouter();

  return (
    <div className="min-h-screen flex" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
      {/* Sidebar */}
      <aside className="w-64 h-screen flex flex-col p-6 fixed" style={{ backgroundColor: '#2D799C' }}>
        
        {/* Logo */}
        <div className="mb-8 flex justify-center">
          <Image 
            src='/sugars.png'
            alt="Sugarsense Logo" 
            width={300} 
            height={150} 
            priority 
          />
        </div>

        {/* Navigation Links */}
        <nav className="flex flex-col space-y-4">
          <Link href="/fitness" className={`p-2 rounded ${router.pathname === '/fitness' ? 'text-white' : 'hover:bg-blue-500'}`} style={{
              backgroundColor: router.pathname === '/fitness' ? '#16384F' : 'transparent',
              color: router.pathname === '/fitness' ? '#FCEDE9' : '#FCEDE9'
            }}>
            Upload Data
          </Link>
          <Link href="/blood" className={`p-2 rounded ${router.pathname === '/blood' ? 'text-white' : 'hover:bg-blue-500'}`} style={{
              backgroundColor: router.pathname === '/blood' ? '#16384F' : 'transparent',
              color: router.pathname === '/blood' ? '#FCEDE9' : '#FCEDE9'
            }}>
            Blood Data
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 ml-64" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
        {children}
      </main>
    </div>
  );
}
