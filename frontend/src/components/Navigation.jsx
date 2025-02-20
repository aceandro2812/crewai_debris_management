import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Construction Debris Management
        </Typography>
        <Box>
          <Button color="inherit" component={Link} to="/">Materials</Button>
          <Button color="inherit" component={Link} to="/analyze">Analyze Debris</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;