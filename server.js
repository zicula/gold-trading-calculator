const express = require('express');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdnjs.cloudflare.com", "fonts.googleapis.com"],
            scriptSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdnjs.cloudflare.com"],
            fontSrc: ["'self'", "fonts.gstatic.com", "fonts.googleapis.com"],
            imgSrc: ["'self'", "data:", "blob:"],
            connectSrc: ["'self'"]
        }
    }
}));

// Enable CORS
app.use(cors());

// Compression middleware
app.use(compression());

// Logging middleware
app.use(morgan('combined'));

// Parse JSON bodies
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Serve static files
app.use(express.static(path.join(__dirname)));

// Main route - serve the lot calculator
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'lot-calculator.html'));
});

// API route for lot calculation (for future API usage)
app.post('/api/calculate-lot', (req, res) => {
    try {
        const { totalCapital, riskPercent, entryPrice, stopLoss, takeProfit, direction } = req.body;
        
        // Validate inputs
        if (!totalCapital || !riskPercent || !entryPrice || !stopLoss || !direction) {
            return res.status(400).json({ 
                error: 'Missing required parameters',
                required: ['totalCapital', 'riskPercent', 'entryPrice', 'stopLoss', 'direction']
            });
        }

        // Constants
        const contractSize = 100; // 100 oz per lot
        
        // Calculate risk amount
        const riskAmount = totalCapital * (riskPercent / 100);
        
        // Calculate stop distance
        let stopDistance;
        if (direction === 'long') {
            stopDistance = entryPrice - stopLoss;
        } else {
            stopDistance = stopLoss - entryPrice;
        }
        
        if (stopDistance <= 0) {
            return res.status(400).json({ 
                error: 'Invalid stop loss for the selected direction' 
            });
        }
        
        // Calculate lot size
        const lotSize = riskAmount / (contractSize * stopDistance);
        const roundedLot = Math.round(lotSize * 10000) / 10000;
        
        // Calculate other values
        const tradeValue = roundedLot * contractSize * entryPrice;
        const actualRisk = roundedLot * contractSize * stopDistance;
        
        let profitAmount = 0;
        let riskRewardRatio = 'N/A';
        
        if (takeProfit) {
            let profitDistance;
            if (direction === 'long') {
                profitDistance = takeProfit - entryPrice;
            } else {
                profitDistance = entryPrice - takeProfit;
            }
            
            if (profitDistance > 0) {
                profitAmount = roundedLot * contractSize * profitDistance;
                riskRewardRatio = `1:${(profitDistance / stopDistance).toFixed(2)}`;
            }
        }
        
        // Return calculation results
        res.json({
            success: true,
            results: {
                lotSize: roundedLot,
                tradeValue: tradeValue,
                riskAmount: actualRisk,
                profitAmount: profitAmount,
                stopDistance: stopDistance,
                riskRewardRatio: riskRewardRatio,
                pipValue: roundedLot * 10 // $10 per pip for 1 lot
            }
        });
        
    } catch (error) {
        console.error('Calculation error:', error);
        res.status(500).json({ 
            error: 'Internal server error during calculation' 
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        service: 'Gold Trading Lot Calculator'
    });
});

// API info endpoint
app.get('/api', (req, res) => {
    res.json({
        name: 'Gold Trading Lot Calculator API',
        version: '1.0.0',
        endpoints: {
            'GET /': 'Main calculator interface',
            'POST /api/calculate-lot': 'Calculate lot size',
            'GET /health': 'Health check',
            'GET /api': 'API information'
        },
        example: {
            url: '/api/calculate-lot',
            method: 'POST',
            body: {
                totalCapital: 10000,
                riskPercent: 2,
                entryPrice: 2000,
                stopLoss: 1990,
                takeProfit: 2020,
                direction: 'long'
            }
        }
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ 
        error: 'Endpoint not found',
        message: 'Please check the URL and try again',
        availableEndpoints: ['/', '/health', '/api', '/api/calculate-lot']
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ 
        error: 'Internal server error',
        message: 'Something went wrong on the server'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🏆 Gold Trading Lot Calculator Server`);
    console.log(`🌐 Server running on port ${PORT}`);
    console.log(`📱 Access the calculator: http://localhost:${PORT}`);
    console.log(`🔗 API endpoint: http://localhost:${PORT}/api`);
    console.log(`❤️  Health check: http://localhost:${PORT}/health`);
    console.log(`⚡ Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received. Shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('SIGINT received. Shutting down gracefully...');
    process.exit(0);
});

module.exports = app;
