import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'TextSum',
  description: 'This is a simple text summarization app',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-[#171717]">
        <div className="overflow-x-hidden lg:p-[100px] sm:p-[75px] xs:p-[50px]">
          {children}
        </div>
      </body>
    </html>
  )
}
