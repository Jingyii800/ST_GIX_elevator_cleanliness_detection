import React from "react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { ActiveAlerts } from "./screens/ActiveAlerts";
import { ConfirmPage } from "./screens/ConfirmPage";
import { DashboardElevator } from "./screens/DashboardElevator";
import { DashboardStation } from "./screens/DashboardStation";
import { ElevatorStatus } from "./screens/ElevatorStatus";
import { ReportLogs } from "./screens/ReportLogs";

const router = createBrowserRouter([
  {
    path: "/dashboard-station",
    element: <DashboardStation />,
  },
  {
    path: "/elevator-status/:stationName/:elevatorId",
    element: <DashboardElevator />,
  },
  {
    path: "/report-logs",
    element: <ReportLogs />
  },
  {
    path: "/elevator-status",
    element: <ElevatorStatus />,
  },
  {
    path: "/confirm-page",
    element: <ConfirmPage />,
  },
  {
    path: "/active-alerts",
    element: <ActiveAlerts />,
  },
  // {
  //   path: "/*",
  //   element: <DashboardStation />,
  // },
]);

export const App = () => {
  return <RouterProvider router={router} />;
};
