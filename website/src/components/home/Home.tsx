import React, { useState } from 'react';
import './Home.css';
import Finder from './finder/Finder';
import { Dialog } from 'primereact/dialog';
import from80to100 from '../../assets/80-100.gif';
import from0to20 from '../../assets/0-20.gif';
import from20to50 from '../../assets/20-50.gif';
import from50to80 from '../../assets/50-80.gif';
import errorImg from '../../assets/200w.gif';
import { NavLink } from 'react-router-dom';

function Home() {
    const [visible, setVisible] = useState<boolean>(false);
    const [sentiment, setSentiment] = useState(-1)
    const [image, setImage] = useState(errorImg)

    const show = (value?: number) => {
        setSentiment(value || -1);
        setImage(getImage(value || -1))
        setVisible(true);
    }

    function getImage(value: number): string {
        if (value < 0) return errorImg
        if (value >= 0.8 && value <= 1) return from80to100
        if (value >= 0.5 && value < 0.8) return from50to80
        if (value >= 0.2 && value < 0.5) return from20to50
        if (value >= 0 && value < 0.2) return from0to20

        return errorImg;
    }

    return (
        <div className="Home">
            <h1>Sentiment Analyzer</h1>
            <div className="Finder">
                <Finder show={show} />
            </div>
            <Dialog visible={visible} onHide={() => setVisible(false)} >
                <div className='dialog'>
                    <h1>{sentiment >= 0 ? Math.round(sentiment * 100) + '%' : 'Site or Entity not found in the database'}</h1>
                    <img src={image} alt="sentiment" className='meme' />
                </div>
            </Dialog>
            <div className='link'>
                <NavLink to='/add'>Add data</NavLink>
            </div>
        </div>
    );
}

export default Home;
