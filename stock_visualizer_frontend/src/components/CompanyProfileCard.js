import React, { useState, useEffect } from 'react';
import { Card, Button } from 'react-bootstrap';

export default function CompanyProfileCard({ symbol }) {
    const [company, setCompany] = useState(null);
    const [expanded, setExpanded] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const toggleExpanded = () => setExpanded(!expanded);

    useEffect(() => {
        if (symbol) {
        setIsLoading(true);
        fetch(`${process.env.REACT_APP_API_URL}/base_data/${symbol}/`)
            .then(response => response.json())
            .then(data => data[0])
            .then(data => {
                setCompany(data);
                setIsLoading(false);
            })
            .catch(error => {
            console.error('Failed to fetch company data', error);
            setError(error);
            setIsLoading(false);
            });
        }
    }, [symbol]);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error loading company data.</div>;
    if (!company) return <div>No company data available.</div>; 

    return (
        <Card>
            <Card.Body>
                <Card.Title>{company.name}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                    {company.sector} - {company.industry}
                </Card.Subtitle>
                <Button variant="primary" onClick={toggleExpanded}>
                    {expanded ? 'Less' : 'More'}
                </Button>

                {expanded && (
                    <>
                        <Card.Text>
                            {company.description}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>Stock Ticker:</strong> {company.symbol}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>Country:</strong> {company.country}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>Currency:</strong> {company.currency}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>Headquarters:</strong> {company.headquarters}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>Fiscal Year End:</strong> {company.fiscal_year_end}
                        </Card.Text>
                        <Card.Text className="mt-2">
                            <strong>CIK:</strong> {company.cik}
                        </Card.Text>
                        {company.is_sp500 && (
                            <Card.Text className="mt-2">
                                <strong>Date Added to S&P 500:</strong> {company.date_added_to_sp500}
                            </Card.Text>
                        )}
                    </>
                )}
            </Card.Body>
        </Card>
    );
}
