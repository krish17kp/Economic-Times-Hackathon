export const validators = {
  required: (val) => !!val || 'This field is required',
  phone: (val) => /^[6-9]\d{9}$/.test(val) || 'Invalid phone number',
  pincode: (val) => /^[1-9][0-9]{5}$/.test(val) || 'Invalid pincode',
};
