# Remotion Reference

> Source: Context7 — /websites/remotion_dev (Remotion official documentation)
> Updated: 2026-03-11

## Core Concepts

Remotion is a React-based framework for creating videos programmatically. Every frame of a video is a React component rendered at a specific point in time.

## useCurrentFrame

Returns the current frame number. This is the most fundamental hook — use it to drive all animations.

```tsx
import { useCurrentFrame } from 'remotion';

const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  return <div>Current frame: {frame}</div>;
};
```

## useVideoConfig

Returns the video configuration: `width`, `height`, `fps`, and `durationInFrames`.

```tsx
import React from 'react';
import { useVideoConfig } from 'remotion';

export const MyComp: React.FC = () => {
  const { width, height, fps, durationInFrames } = useVideoConfig();
  console.log(width);            // 1920
  console.log(height);           // 1080
  console.log(fps);              // 30
  console.log(durationInFrames); // 300

  return <div>Hello World!</div>;
};
```

## Interpolation

`interpolate()` maps a value from one range to another. Essential for animations.

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

const translateY = interpolate(frame, [0, 30], [50, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### Extrapolation Options

| Option | Description |
|--------|-------------|
| `'extend'` | Continue the interpolation beyond the range (default) |
| `'clamp'` | Clamp the output to the output range |
| `'identity'` | Return the input value as-is |

## Spring Animations

Physics-based animations that feel natural.

### Basic Spring

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const value = spring({
  frame,
  fps,
  config: {
    stiffness: 100,
  },
});
```

### Spring with Duration

Stretches the animation to a specific number of frames.

```tsx
const value = spring({
  frame,
  fps,
  config: {
    stiffness: 100,
  },
  durationInFrames: 40,
});
```

### Spring with Delay

```tsx
const scale = spring({
  fps,
  frame: frame - 10,  // delay by 10 frames
  config: {
    damping: 100,
  },
});
```

### Spring Config Options

| Option | Default | Description |
|--------|---------|-------------|
| `stiffness` | 100 | Higher = faster, more "snappy" |
| `damping` | 10 | Higher = less oscillation |
| `mass` | 1 | Higher = slower, more inertia |
| `overshootClamping` | false | Prevent overshooting target |

## Complete Composition Example

A full example combining `useCurrentFrame`, `useVideoConfig`, `spring`, and `interpolate`.

```tsx
import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

type Props = {
  name: string;
  logo: string;
  repo: string;
};

export const MyComposition: React.FC<Props> = ({ name, repo, logo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    fps,
    frame: frame - 10,
    config: {
      damping: 100,
    },
  });

  const opacity = interpolate(frame, [30, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const moveY = interpolate(frame, [20, 30], [10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        scale: String(scale),
        backgroundColor: 'white',
        fontWeight: 'bold',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: 20 }}>
        <Img src={logo} style={{ height: 80 }} />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div style={{ fontSize: 40, transform: `translateY(${moveY}px)`, lineHeight: 1 }}>
            {name}
          </div>
          <div style={{ fontSize: 20, opacity, lineHeight: 1.25 }}>
            {repo}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

## Composition Setup

Register compositions in `Root.tsx` using the `<Composition>` component.

```tsx
import React from 'react';
import { Composition } from 'remotion';
import { MyComposition } from './MyComposition';

export const Root: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyComposition}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={300}
      defaultProps={{
        name: 'My Project',
        logo: 'https://example.com/logo.png',
        repo: 'user/repo',
      }}
    />
  );
};
```

### Dynamic Duration with calculateMetadata

Calculate composition duration dynamically based on props (e.g., video lengths).

```tsx
import { CalculateMetadataFunction } from 'remotion';
import { parseMedia } from '@remotion/media-parser';

type Props = {
  videos: { src: string; durationInFrames: number | null }[];
};

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const fps = 30;
  const videos = await Promise.all(
    props.videos.map(async (video) => {
      const { slowDurationInSeconds } = await parseMedia({
        src: video.src,
        fields: { slowDurationInSeconds: true },
      });
      return {
        durationInFrames: Math.floor(slowDurationInSeconds * fps),
        src: video.src,
      };
    })
  );

  const totalDurationInFrames = videos.reduce(
    (acc, video) => acc + video.durationInFrames!,
    0
  );

  return {
    props: { ...props, videos },
    fps,
    durationInFrames: totalDurationInFrames,
  };
};
```

## Sequences

`<Sequence>` offsets content in time. Everything inside starts at frame 0 relative to the sequence.

```tsx
import { Sequence } from 'remotion';

const MyVideo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={60}>
        <Title />
      </Sequence>
      <Sequence from={60} durationInFrames={120}>
        <Content />
      </Sequence>
      <Sequence from={180}>
        <Outro />
      </Sequence>
    </AbsoluteFill>
  );
};
```

## Series

`<Series>` places sequences one after another automatically (no manual `from` calculation).

```tsx
import { Series, OffthreadVideo, staticFile } from 'remotion';

export const VideosInSequence: React.FC<Props> = ({ videos }) => {
  return (
    <Series>
      {videos.map((vid) => (
        <Series.Sequence key={vid.src} durationInFrames={vid.durationInFrames}>
          <OffthreadVideo src={vid.src} />
        </Series.Sequence>
      ))}
    </Series>
  );
};
```

### Series vs Sequence

| Feature | `<Sequence>` | `<Series>` |
|---------|-------------|-----------|
| Timing | Manual `from` prop | Automatic, sequential |
| Overlap | Possible | No overlap |
| Gap | Manual calculation | Built-in offset prop |
| Use case | Complex timelines | Simple linear sequences |

## Audio

```tsx
import { Audio, staticFile } from 'remotion';

const MyVideo: React.FC = () => {
  return (
    <>
      <Audio src={staticFile('background-music.mp3')} volume={0.5} />
      <Sequence from={30}>
        <Audio src={staticFile('sound-effect.mp3')} />
      </Sequence>
    </>
  );
};
```

### Volume Automation

```tsx
<Audio
  src={staticFile('music.mp3')}
  volume={(f) =>
    interpolate(f, [0, 30, 270, 300], [0, 0.8, 0.8, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  }
/>
```

## AbsoluteFill

A full-size container with `position: absolute` that fills the composition.

```tsx
import { AbsoluteFill } from 'remotion';

const MyScene: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'white', justifyContent: 'center', alignItems: 'center' }}>
      <h1>Hello</h1>
    </AbsoluteFill>
  );
};
```

## Static Files

Use `staticFile()` to reference files in the `public/` directory.

```tsx
import { staticFile, Img, Audio, Video } from 'remotion';

<Img src={staticFile('logo.png')} />
<Audio src={staticFile('music.mp3')} />
<Video src={staticFile('intro.mp4')} />
```

## OffthreadVideo

More performant than `<Video>` — renders video frames without using an HTML `<video>` element.

```tsx
import { OffthreadVideo, staticFile } from 'remotion';

<OffthreadVideo src={staticFile('video.mp4')} />
```

## Player Component

Embed a Remotion composition in a React app (for previewing, not rendering).

```tsx
import { Player } from '@remotion/player';
import { MyComposition } from './MyComposition';

const App: React.FC = () => {
  return (
    <Player
      component={MyComposition}
      durationInFrames={300}
      compositionWidth={1920}
      compositionHeight={1080}
      fps={30}
      controls
      style={{ width: '100%' }}
      inputProps={{
        name: 'My Video',
        logo: '/logo.png',
        repo: 'user/repo',
      }}
    />
  );
};
```

### Player Props

| Prop | Description |
|------|-------------|
| `component` | React component to render |
| `durationInFrames` | Total frames |
| `compositionWidth/Height` | Video dimensions |
| `fps` | Frames per second |
| `controls` | Show playback controls |
| `loop` | Loop playback |
| `autoPlay` | Start playing automatically |
| `clickToPlay` | Click to toggle play/pause |
| `inputProps` | Props passed to the component |
| `style` | CSS styles for the player container |

## Rendering

### CLI Rendering

```bash
# Render a specific composition
npx remotion render src/index.ts MyVideo out/video.mp4

# Render with custom props
npx remotion render src/index.ts MyVideo out/video.mp4 --props='{"name":"Test"}'

# Render as GIF
npx remotion render src/index.ts MyVideo out/animation.gif

# Render still image
npx remotion still src/index.ts MyVideo out/thumbnail.png --frame=50
```

### Programmatic Rendering

```tsx
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';

const bundled = await bundle(require.resolve('./src/index'));

const composition = await selectComposition({
  serveUrl: bundled,
  id: 'MyVideo',
});

await renderMedia({
  composition,
  serveUrl: bundled,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
});
```

## Lambda Rendering

Render videos in AWS Lambda for scalable, serverless rendering.

```tsx
import { renderMediaOnLambda } from '@remotion/lambda/client';

const { renderId, bucketName } = await renderMediaOnLambda({
  region: 'us-east-1',
  functionName: 'remotion-render',
  composition: 'MyVideo',
  serveUrl: 'https://my-site.com/bundle',
  codec: 'h264',
  inputProps: { name: 'Test' },
});
```

## Transitions

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

const MyVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={60}>
        <Scene1 />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />
      <TransitionSeries.Sequence durationInFrames={60}>
        <Scene2 />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={slide({ direction: 'from-left' })}
        timing={linearTiming({ durationInFrames: 20 })}
      />
      <TransitionSeries.Sequence durationInFrames={60}>
        <Scene3 />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

### Available Transitions

| Transition | Import | Description |
|-----------|--------|-------------|
| `fade()` | `@remotion/transitions/fade` | Crossfade |
| `slide()` | `@remotion/transitions/slide` | Slide in/out |
| `wipe()` | `@remotion/transitions/wipe` | Wipe effect |
| `flip()` | `@remotion/transitions/flip` | 3D flip |
| `clockWipe()` | `@remotion/transitions/clock-wipe` | Clock wipe |

## Common Patterns

### Fade In/Out

```tsx
const frame = useCurrentFrame();
const { durationInFrames } = useVideoConfig();

const opacity = interpolate(
  frame,
  [0, 20, durationInFrames - 20, durationInFrames],
  [0, 1, 1, 0],
  { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
);
```

### Staggered Animations

```tsx
const items = ['React', 'Remotion', 'Video'];

items.map((item, i) => {
  const delay = i * 10;
  const scale = spring({
    frame: frame - delay,
    fps,
    config: { damping: 100 },
  });
  return <div style={{ transform: `scale(${scale})` }}>{item}</div>;
});
```

### Typewriter Effect

```tsx
const frame = useCurrentFrame();
const text = 'Hello, World!';
const charsShown = Math.min(text.length, Math.floor(frame / 2));
const displayText = text.slice(0, charsShown);
```

## Key Packages

| Package | Purpose |
|---------|---------|
| `remotion` | Core framework |
| `@remotion/player` | Embed compositions in React apps |
| `@remotion/renderer` | Programmatic rendering |
| `@remotion/lambda` | AWS Lambda rendering |
| `@remotion/transitions` | Transition effects |
| `@remotion/media-parser` | Parse media file metadata |
| `@remotion/gif` | GIF support |
| `@remotion/lottie` | Lottie animation support |
| `@remotion/three` | Three.js integration |
| `@remotion/noise` | Perlin/simplex noise |
| `@remotion/paths` | SVG path utilities |
| `@remotion/shapes` | SVG shape components |
