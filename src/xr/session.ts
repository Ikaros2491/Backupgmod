/** Shared WebXR session helpers for the VR prototype. */

export async function supportsSession(mode: XRSessionMode): Promise<boolean> {
  if (!navigator.xr) return false;
  try {
    return await navigator.xr.isSessionSupported(mode);
  } catch {
    return false;
  }
}

export function attachGamepadsToControllers(
  session: XRSession,
  assign: (source: XRInputSource) => void,
): void {
  for (const source of session.inputSources) {
    assign(source);
  }
  session.addEventListener("inputsourceschange", (event) => {
    for (const source of event.added) {
      assign(source);
    }
  });
}
