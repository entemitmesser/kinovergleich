import Link from "next/link";
import MovieTable from "~/components/movie-table";

export default function HomePage() {
  return (
    <main className="bg-background flex min-h-screen flex-col items-center">
      <MovieTable />
    </main>
  );
}
