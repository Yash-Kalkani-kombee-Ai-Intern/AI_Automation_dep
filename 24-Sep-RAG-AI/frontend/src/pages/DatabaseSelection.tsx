import {
  ArrowRight,
  Database,
  Lock,
  Sparkles,
  Zap,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface DatabaseSelectionProps {
  onContinue: () => void;
}

export default function DatabaseSelection({
  onContinue,
}: DatabaseSelectionProps) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background grid-background px-6 py-12">
      
      {/* Background glow */}
      <div className="pointer-events-none absolute left-1/2 top-1/4 h-96 w-96 -translate-x-1/2 rounded-full bg-white/[0.03] blur-3xl" />

      <div className="relative z-10 w-full max-w-2xl">

        {/* Logo */}
        <div className="mb-10 flex justify-center">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-secondary">
              <Sparkles className="h-5 w-5 text-zinc-200" />
            </div>

            <span className="text-lg font-semibold tracking-tight text-foreground">
              Local<span className="text-zinc-400">AI</span>
            </span>
          </div>
        </div>

        {/* Main Card */}
        <Card className="glass border-border/70 shadow-2xl shadow-black/40">

          <CardHeader className="pb-4 pt-8 text-center">
            <Badge className="mx-auto mb-4 w-fit border-zinc-700 bg-zinc-800/60 text-zinc-300">
              Private AI Workspace
            </Badge>

            <CardTitle className="text-3xl font-semibold tracking-tight sm:text-4xl">
              Welcome to{" "}
              <span className="gradient-text">
                LocalAI
              </span>
            </CardTitle>

            <CardDescription className="mx-auto mt-3 max-w-md text-base leading-6 text-muted-foreground">
              Connect your AI assistant to a configured
              database and ask questions using natural language.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6 pb-8">

            {/* Database option */}
            <div className="rounded-xl border border-border bg-secondary/40 p-4 transition-colors hover:border-zinc-500/40">
              <div className="flex items-center gap-4">

                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-border bg-background">
                  <Database className="h-5 w-5 text-zinc-200" />
                </div>

                <div className="flex-1">
                  <p className="font-medium text-foreground">
                    Restaurant Database
                  </p>

                  <p className="mt-1 text-sm text-muted-foreground">
                    MySQL • Restaurant AI workspace
                  </p>
                </div>

                <div className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.6)]" />
              </div>
            </div>

            {/* Continue */}
            <Button
              onClick={onContinue}
              size="lg"
              className="group h-12 w-full font-medium"
            >
              Continue to Workspace

              <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Button>

            {/* Features */}
            <div className="grid grid-cols-3 gap-3 pt-2">

              <div className="flex flex-col items-center gap-2 rounded-lg border border-border/70 bg-secondary/20 p-3 text-center">
                <Lock className="h-4 w-4 text-muted-foreground" />

                <span className="text-xs text-muted-foreground">
                  Private
                </span>
              </div>

              <div className="flex flex-col items-center gap-2 rounded-lg border border-border/70 bg-secondary/20 p-3 text-center">
                <Zap className="h-4 w-4 text-muted-foreground" />

                <span className="text-xs text-muted-foreground">
                  Local AI
                </span>
              </div>

              <div className="flex flex-col items-center gap-2 rounded-lg border border-border/70 bg-secondary/20 p-3 text-center">
                <Database className="h-4 w-4 text-muted-foreground" />

                <span className="text-xs text-muted-foreground">
                  SQL Powered
                </span>
              </div>

            </div>

          </CardContent>
        </Card>

        <p className="mt-6 text-center text-xs text-muted-foreground">
          Your data stays inside your configured environment.
        </p>
      </div>
    </div>
  );
}