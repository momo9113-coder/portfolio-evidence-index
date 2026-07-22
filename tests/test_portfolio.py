import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PortfolioIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.portfolio = json.loads((ROOT / "portfolio.json").read_text(encoding="utf-8"))
        cls.schema = json.loads((ROOT / "portfolio.schema.json").read_text(encoding="utf-8"))
        cls.inventory = json.loads(
            (ROOT / "generated" / "github-repositories.json").read_text(encoding="utf-8")
        )

    def test_expected_project_routes_are_present(self) -> None:
        routes = self.portfolio["project_routes"]
        ids = {route["id"] for route in routes}
        self.assertEqual(
            ids,
            {
                "rogii-wellbore-geology-portfolio",
                "loadlens-forecasting-service",
                "commercelens-analytics-warehouse",
            },
        )
        self.assertTrue(all(route["resume_eligible"] for route in routes))

    def test_routed_projects_exist_in_complete_inventory(self) -> None:
        inventory_names = {
            repository["full_name"] for repository in self.inventory["repositories"]
        }
        for route in self.portfolio["project_routes"]:
            self.assertIn(route["repository"], inventory_names)

    def test_forks_are_not_routed_as_authored_projects(self) -> None:
        fork_names = {
            repository["full_name"]
            for repository in self.inventory["repositories"]
            if repository["is_fork"]
        }
        authored_names = {
            route["repository"] for route in self.portfolio["project_routes"]
        }
        self.assertTrue(fork_names.isdisjoint(authored_names))
        self.assertIn("momo9113-coder/hajiren", fork_names)

    def test_each_route_requires_independent_inspection(self) -> None:
        for route in self.portfolio["project_routes"]:
            self.assertTrue(route["read_first"])
            self.assertTrue(route["inspect_next"])
            self.assertTrue(route["evaluate_for"])
            self.assertIn("README.md", route["read_first"])

    def test_public_documents_do_not_duplicate_project_metrics(self) -> None:
        self.assertNotIn("metrics", self.portfolio)
        for route in self.portfolio["project_routes"]:
            self.assertNotIn("metrics", route)
            self.assertNotIn("approved_claims", route)

    def test_public_documents_do_not_contain_local_paths_or_secrets(self) -> None:
        files = [
            ROOT / "portfolio.json",
            ROOT / "portfolio.schema.json",
            ROOT / "llms.txt",
            ROOT / "generated" / "github-repositories.json",
        ]
        disallowed = ["C:\\Users", "ghp_", "github_pat_", "kaggle.json"]
        for path in files:
            content = path.read_text(encoding="utf-8")
            for value in disallowed:
                self.assertNotIn(value, content, f"{value!r} found in {path.name}")


if __name__ == "__main__":
    unittest.main()
