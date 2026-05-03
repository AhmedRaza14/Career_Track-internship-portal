import '../styles/globals.css';
import { GoogleOAuthProvider } from '@react-oauth/google';

export const metadata = {
  title: 'CareerTrack - Build Your Professional Profile',
  description: 'Connect with recruiters, find jobs, and collaborate with students',
};

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
          {children}
        </GoogleOAuthProvider>
      </body>
    </html>
  );
}
