import React, { useState } from 'react';
import { Card, CardContent, TextField, Button, Typography, Box } from '@mui/material';
import axios from 'axios';

const MaterialForm = ({ onMaterialAdded }) => {
  const [material, setMaterial] = useState({ material_name: '', weight: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/materials/', material);
      setMaterial({ material_name: '', weight: '' });
      onMaterialAdded();
    } catch (error) {
      console.error('Error adding material:', error);
    }
  };

  return (
    <Card sx={{ maxWidth: 600, margin: '20px auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Add Construction Material
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Material Name"
            value={material.material_name}
            onChange={(e) => setMaterial({ ...material, material_name: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Weight (kg)"
            type="number"
            value={material.weight}
            onChange={(e) => setMaterial({ ...material, weight: e.target.value })}
            margin="normal"
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
          >
            Add Material
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MaterialForm;