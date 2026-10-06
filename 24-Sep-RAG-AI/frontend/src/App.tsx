import { useState } from "react";

import DatabaseSelection from "@/pages/DatabaseSelection";
import Chat from "@/pages/Chat";

function App() {
  const [databaseSelected, setDatabaseSelected] =
    useState(false);

  if (!databaseSelected) {
    return (
      <DatabaseSelection
        onContinue={() => setDatabaseSelected(true)}
      />
    );
  }

  return <Chat />;
}

export default App;