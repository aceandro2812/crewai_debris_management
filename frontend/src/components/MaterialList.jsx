import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import axios from 'axios';

const MaterialList = ({ refreshTrigger }) => {
  const [materials, setMaterials] = useState([]);

  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const response = await axios.get('http://localhost:8000/materials/');
        setMaterials(response.data);
      } catch (error) {
        console.error('Error fetching materials:', error);
      }
    };
    fetchMaterials();
  }, [refreshTrigger]);

  return (
    <Card sx={{ maxWidth: 600, margin: '20px auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Construction Materials
        </Typography>
        <List>
          {materials.map((material, index) => (
            <React.Fragment key={material.id}>
              <ListItem>
                <ListItemText
                  primary={material.material_name}
                  secondary={`Weight: ${material.weight} kg`}
                />
              </ListItem>
              {index < materials.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default MaterialList;