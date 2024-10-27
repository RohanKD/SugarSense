import Image from 'next/image';
import Link from 'next/link';
import { FC } from 'react';

const Home: FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen" style={{ backgroundColor: '#FCEDE9', color: '#2D799C' }}>
      {/* Logo */}
      <Image
        src="/sugarsblue.png"
        alt="SUGARSENSE Logo"
        width={300}
        height={100}
        className="mb-8"
        priority
      />

      {/* Placeholder Quote */}
      <blockquote className="text-center text-lg italic" style={{ color: '#2D799C' }}>
        "Helping diabetics since 2024."
      </blockquote>

      {/* Login Button */}
      <Link href="/fitness">
        <button
          className="px-6 py-3 mt-8 font-semibold rounded transition duration-200"
          style={{ backgroundColor: '#2D799C', color: '#FCEDE9' }}
        >
          SUGARSENSE
        </button>
      </Link>
    </div>
  );
};

export default Home;
