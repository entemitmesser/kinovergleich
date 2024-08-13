import Link from "next/link";
import LustigeListe from "~/components/lustige-liste";
import MovieTable from "~/components/movie-table";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <MovieTable />
    </main>
  );
}
