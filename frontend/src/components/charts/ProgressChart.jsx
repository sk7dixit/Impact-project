import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

const data = [
  { day: "Mon", score: 60 },
  { day: "Tue", score: 70 },
  { day: "Wed", score: 75 },
  { day: "Thu", score: 80 },
  { day: "Fri", score: 90 },
];

function ProgressChart() {
  return (
    <LineChart width={600} height={300} data={data}>

      <CartesianGrid strokeDasharray="3 3" />

      <XAxis dataKey="day" />

      <YAxis />

      <Tooltip />

      <Line
        type="monotone"
        dataKey="score"
        stroke="#2563eb"
      />

    </LineChart>
  );
}

export default ProgressChart;