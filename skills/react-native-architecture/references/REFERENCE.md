# React Native Architecture — Reference Documentation

> Source: Context7 (reactnative_dev, facebook/react-native-website) | Updated: 2026-03-11

---

## Table of Contents

- [Project Setup with Expo](#project-setup-with-expo)
- [Turbo Native Modules](#turbo-native-modules)
- [Native Modules (Legacy)](#native-modules-legacy)
- [New Architecture](#new-architecture)
- [FlatList](#flatlist)
- [Flexbox Layout](#flexbox-layout)
- [Animations — LayoutAnimation](#animations--layoutanimation)
- [Animations — Animated API with ScrollView](#animations--animated-api-with-scrollview)
- [Testing](#testing)
- [Hermes Engine](#hermes-engine)
- [Android Configuration](#android-configuration)

---

## Project Setup with Expo

Initialize a new React Native project using Expo:

```shell
npx create-expo-app@latest
```

This sets up a production-grade React Native framework with file-based routing, native module libraries pre-configured, and all necessary tooling.

---

## Turbo Native Modules

Full example integrating a custom `NativeLocalStorage` Turbo Native Module:

```typescript
import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  Button,
} from 'react-native';

import NativeLocalStorage from './specs/NativeLocalStorage';

const EMPTY = '<empty>';

function App(): React.JSX.Element {
  const [value, setValue] = React.useState<string | null>(null);
  const [editingValue, setEditingValue] = React.useState<string | null>(null);

  React.useEffect(() => {
    const storedValue = NativeLocalStorage?.getItem('myKey');
    setValue(storedValue ?? '');
  }, []);

  function saveValue() {
    NativeLocalStorage?.setItem(editingValue ?? EMPTY, 'myKey');
    setValue(editingValue);
  }

  function clearAll() {
    NativeLocalStorage?.clear();
    setValue('');
  }

  function deleteValue() {
    NativeLocalStorage?.removeItem('myKey');
    setValue('');
  }

  return (
    <SafeAreaView style={{flex: 1}}>
      <Text style={styles.text}>
        Current stored value is: {value ?? 'No Value'}
      </Text>
      <TextInput
        placeholder="Enter the text you want to store"
        style={styles.textInput}
        onChangeText={setEditingValue}
      />
      <Button title="Save" onPress={saveValue} />
      <Button title="Delete" onPress={deleteValue} />
      <Button title="Clear" onPress={clearAll} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  text: { margin: 10, fontSize: 20 },
  textInput: {
    margin: 10, height: 40, borderColor: 'black',
    borderWidth: 1, paddingLeft: 5, paddingRight: 5, borderRadius: 5,
  },
});

export default App;
```

---

## Native Modules (Legacy)

Import NativeModules to access exported native modules from JavaScript:

```tsx
import {NativeModules} from 'react-native';
```

---

## New Architecture

### Synchronous Communication via JSI

The new architecture enables synchronous native calls, returning native object references directly:

```typescript
// Sync response from Native Module
const value = nativeModule.getValue();

// value can be a reference to a native object
nativeModule.doSomething(value);
```

**Key benefits:**
- Direct JSI calls (no bridge serialization)
- Synchronous returns from native
- Native object references in JS
- Fabric renderer for concurrent features
- TurboModules for lazy-loaded native modules

### Gradle Properties for New Architecture

```diff
+reactNativeArchitectures=armeabi-v7a,arm64-v8a,x86,x86_64
+newArchEnabled=true
+hermesEnabled=true
```

### Android Host Configuration (Kotlin)

```kotlin
override val reactNativeHost: ReactNativeHost =
    object : DefaultReactNativeHost(this) {
        override fun getPackages(): List<ReactPackage> =
            PackageList(this).packages.apply {
                add(NativeLocalStoragePackage())
            }

        override fun getJSMainModuleName(): String = "index"
        override fun getUseDeveloperSupport(): Boolean = BuildConfig.DEBUG
        override val isNewArchEnabled: Boolean = BuildConfig.IS_NEW_ARCHITECTURE_ENABLED
        override val isHermesEnabled: Boolean = BuildConfig.IS_HERMES_ENABLED
    }

override val reactHost: ReactHost
    get() = getDefaultReactHost(applicationContext, reactNativeHost)

override fun onCreate() {
    super.onCreate()
    SoLoader.init(this, false)
    if (BuildConfig.IS_NEW_ARCHITECTURE_ENABLED) {
        load()
    }
}
```

---

## FlatList

### With ItemSeparatorComponent and renderItem

```TypeScript
<FlatList
  ItemSeparatorComponent={
    Platform.OS !== 'android' &&
    (({highlighted}) => (
      <View
        style={[style.separator, highlighted && {marginLeft: 0}]}
      />
    ))
  }
  data={[{title: 'Title Text', key: 'item1'}]}
  renderItem={({item, index, separators}) => (
    <TouchableHighlight
      key={item.key}
      onPress={() => this._onPress(item)}
      onShowUnderlay={separators.highlight}
      onHideUnderlay={separators.unhighlight}>
      <View style={{backgroundColor: 'white'}}>
        <Text>{item.title}</Text>
      </View>
    </TouchableHighlight>
  )}
/>
```

**Key FlatList props:**
- `data` — array of items
- `renderItem` — function receiving `{item, index, separators}`
- `keyExtractor` — function to extract unique key
- `ItemSeparatorComponent` — rendered between items
- `ListHeaderComponent`, `ListFooterComponent`
- `onEndReached`, `onEndReachedThreshold` — infinite scroll
- `refreshing`, `onRefresh` — pull-to-refresh
- `getItemLayout` — optimization for known item sizes
- `initialNumToRender`, `maxToRenderPerBatch`, `windowSize`

---

## Flexbox Layout

### FlexDirection

```javascript
import React, {useState} from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';

const FlexDirectionBasics = () => {
  const [flexDirection, setflexDirection] = useState('column');

  return (
    <PreviewLayout
      label="flexDirection"
      values={['column', 'row', 'row-reverse', 'column-reverse']}
      selectedValue={flexDirection}
      setSelectedValue={setflexDirection}>
      <View style={[styles.box, {backgroundColor: 'powderblue'}]} />
      <View style={[styles.box, {backgroundColor: 'skyblue'}]} />
      <View style={[styles.box, {backgroundColor: 'steelblue'}]} />
    </PreviewLayout>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, marginTop: 8, backgroundColor: 'aliceblue' },
  box: { width: 50, height: 50 },
  row: { flexDirection: 'row', flexWrap: 'wrap' },
  button: {
    paddingHorizontal: 8, paddingVertical: 6, borderRadius: 4,
    backgroundColor: 'oldlace', alignSelf: 'flex-start',
    marginHorizontal: '1%', marginBottom: 6, minWidth: '48%', textAlign: 'center',
  },
  selected: { backgroundColor: 'coral', borderWidth: 0 },
  buttonLabel: { fontSize: 12, fontWeight: '500', color: 'coral' },
  selectedLabel: { color: 'white' },
  label: { textAlign: 'center', marginBottom: 10, fontSize: 24 },
});
```

**Key flexbox properties:**
- `flexDirection`: `'column'` (default), `'row'`, `'row-reverse'`, `'column-reverse'`
- `justifyContent`: `'flex-start'`, `'center'`, `'flex-end'`, `'space-between'`, `'space-around'`, `'space-evenly'`
- `alignItems`: `'stretch'` (default), `'flex-start'`, `'center'`, `'flex-end'`, `'baseline'`
- `flexWrap`: `'nowrap'` (default), `'wrap'`, `'wrap-reverse'`
- `flex`: shorthand for `flexGrow`, `flexShrink`, `flexBasis`
- `gap`, `rowGap`, `columnGap`: spacing between children

---

## Animations — LayoutAnimation

Animate layout changes with `LayoutAnimation.configureNext`:

```tsx
import React, {useState} from 'react';
import {
  View, Platform, UIManager, LayoutAnimation, StyleSheet, Button,
} from 'react-native';

if (
  Platform.OS === 'android' &&
  UIManager.setLayoutAnimationEnabledExperimental
) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

const App = () => {
  const [boxPosition, setBoxPosition] = useState('left');

  const toggleBox = () => {
    LayoutAnimation.configureNext({
      duration: 500,
      create: {type: 'linear', property: 'opacity'},
      update: {type: 'spring', springDamping: 0.4},
      delete: {type: 'linear', property: 'opacity'},
    });
    setBoxPosition(boxPosition === 'left' ? 'right' : 'left');
  };

  return (
    <View style={styles.container}>
      <View style={styles.buttonContainer}>
        <Button title="Toggle Layout" onPress={toggleBox} />
      </View>
      <View style={[styles.box, boxPosition === 'left' ? null : styles.moveRight]} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'flex-start', justifyContent: 'center' },
  box: { height: 100, width: 100, borderRadius: 5, margin: 8, backgroundColor: 'blue' },
  moveRight: { alignSelf: 'flex-end', height: 200, width: 200 },
  buttonContainer: { alignSelf: 'center' },
});

export default App;
```

**Note:** On Android, requires `UIManager.setLayoutAnimationEnabledExperimental(true)`.

---

## Animations — Animated API with ScrollView

Horizontal carousel with animated pagination dots:

```javascript
import React from 'react';
import {
  ScrollView, Text, StyleSheet, View, ImageBackground,
  Animated, useWindowDimensions, useAnimatedValue,
} from 'react-native';
import {SafeAreaView, SafeAreaProvider} from 'react-native-safe-area-context';

const images = new Array(6).fill(
  'https://images.unsplash.com/photo-1556740749-887f6717d7e4',
);

const App = () => {
  const scrollX = useAnimatedValue(0);
  const {width: windowWidth} = useWindowDimensions();

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <View style={styles.scrollContainer}>
          <ScrollView
            horizontal pagingEnabled
            showsHorizontalScrollIndicator={false}
            onScroll={Animated.event([{
              nativeEvent: { contentOffset: { x: scrollX } },
            }])}
            scrollEventThrottle={1}>
            {images.map((image, imageIndex) => (
              <View style={{width: windowWidth, height: 250}} key={imageIndex}>
                <ImageBackground source={{uri: image}} style={styles.card}>
                  <View style={styles.textContainer}>
                    <Text style={styles.infoText}>{'Image - ' + imageIndex}</Text>
                  </View>
                </ImageBackground>
              </View>
            ))}
          </ScrollView>
          <View style={styles.indicatorContainer}>
            {images.map((image, imageIndex) => {
              const width = scrollX.interpolate({
                inputRange: [
                  windowWidth * (imageIndex - 1),
                  windowWidth * imageIndex,
                  windowWidth * (imageIndex + 1),
                ],
                outputRange: [8, 16, 8],
                extrapolate: 'clamp',
              });
              return <Animated.View key={imageIndex} style={[styles.normalDot, {width}]} />;
            })}
          </View>
        </View>
      </SafeAreaView>
    </SafeAreaProvider>
  );
};
```

---

## Testing

### React Native Testing Library — User Interactions

```tsx
test('given empty GroceryShoppingList, user can add an item to it', () => {
  const {getByPlaceholderText, getByText, getAllByText} = render(
    <GroceryShoppingList />,
  );

  fireEvent.changeText(
    getByPlaceholderText('Enter grocery item'),
    'banana',
  );
  fireEvent.press(getByText('Add the item to list'));

  const bananaElements = getAllByText('banana');
  expect(bananaElements).toHaveLength(1);
});
```

**Testing best practices:**
- Use React Native Testing Library for component tests
- `fireEvent.changeText()` for TextInput
- `fireEvent.press()` for Button/Touchable
- `getByText`, `getByPlaceholderText`, `getByTestId` for queries
- `getAllByText` when multiple elements expected
- Test user behavior, not implementation details

---

## Hermes Engine

### Enable on iOS (Podfile)

```ruby
use_react_native!(
   :path => config[:reactNativePath],
   :hermes_enabled => true
)
```

### Build for Android

```bash
./gradlew :ReactAndroid:hermes-engine:assembleDebug
./gradlew :ReactAndroid:hermes-engine:assembleRelease
```

**Hermes benefits:**
- Optimized for React Native
- Reduced memory usage
- Smaller download size
- Faster time to interactive
- Bytecode precompilation

---

## Android Configuration

### Gradle Properties

```properties
reactNativeArchitectures=armeabi-v7a,arm64-v8a,x86,x86_64
newArchEnabled=true
hermesEnabled=true
```

**Architecture options:**
- `armeabi-v7a` — 32-bit ARM
- `arm64-v8a` — 64-bit ARM (most modern devices)
- `x86` — Intel 32-bit (emulator)
- `x86_64` — Intel 64-bit (emulator)
