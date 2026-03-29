import React, { useState } from 'react';
import Header from '../components/Header';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Button from '../components/ui/Button';

export default function Register() {
  const [form, setForm] = useState({ name: '', phone: '', role: 'farmer' });
  return (
    <div className="min-h-screen bg-gray-50 pt-10">
      <Header title="Register" />
      <div className="max-w-md mx-auto p-4 mt-10">
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-6 text-center">Create AgroAI Account</h2>
          <form className="space-y-4" onSubmit={e => e.preventDefault()}>
            <Input label="Full Name" placeholder="e.g. Rajesh Kumar" />
            <Input label="Phone Number" type="tel" placeholder="e.g. 9876543210" />
            <Select 
              label="I am a" 
              options={[
                { value: 'farmer', label: 'Farmer' },
                { value: 'buyer', label: 'Buyer / Industry' }
              ]} 
              value={form.role}
              onChange={e => setForm({...form, role: e.target.value})}
            />
            <Button className="w-full mt-4">Register Account</Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
