import { render, screen } from '@testing-library/react';
import App from './App';

test('renders loan approval engine heading', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /loan approval engine/i })).toBeInTheDocument();
});
