import axios from 'axios';

export default async function handler(req, res) {
    if (req.method === 'POST') {
        try {
            const response = await axios.post('https://your-vercel-deployment-url.vercel.app/chat', req.body, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            res.status(200).json(response.data);
        } catch (error) {
            res.status(500).json({ error: 'Error communicating with the chatbot server.' });
        }
    } else {
        res.status(405).json({ error: 'Method not allowed' });
    }
}
