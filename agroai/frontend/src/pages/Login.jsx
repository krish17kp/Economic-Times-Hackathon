import React, { useState } from 'react';
import Header from '../components/Header';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

export default function Login() {
  const [phone, setPhone] = useState('');
  return (
    <div className="min-h-screen bg-gray-50 pt-10">
      <Header title="Login" />
      <div className="max-w-md mx-auto p-4 mt-10">
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-6 text-center">Welcome Back</h2>
          <form className="space-y-4" onSubmit={e => e.preventDefault()}>
            <Input 
              label="Phone Number" 
              type="tel" 
              placeholder="e.g. 9876543210" 
              value={phone} 
              onChange={e => setPhone(e.target.value)}
            />
            <Button className="w-full">Send OTP</Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
