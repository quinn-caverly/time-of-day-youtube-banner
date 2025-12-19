# Minecraft Time to Hour Mapping

If you want to map Minecraft's day/night cycle to your banner images, here's how:

## Minecraft Time System

- **1 Minecraft day = 24,000 ticks**
- **1 Minecraft hour = 1,000 ticks** (24,000 ÷ 24)

## In-Game Time Mapping

Minecraft's day cycle:
- **0 ticks** (6:00 AM in-game) - Dawn
- **6,000 ticks** (12:00 PM in-game) - Noon  
- **12,000 ticks** (6:00 PM in-game) - Sunset
- **18,000 ticks** (12:00 AM in-game) - Midnight
- **24,000 ticks** - Cycle repeats

## Real-World Time Mapping (Current Script)

The script uses **real-world time**:
- `00.png` = Midnight (00:00) in your timezone
- `06.png` = 6 AM
- `12.png` = Noon (12:00)
- `18.png` = 6 PM (18:00)
- `23.png` = 11 PM (23:00)

## Converting Minecraft Time to Hour

If you want to use Minecraft time instead of real-world time:

```python
minecraft_time = 12000  # Example: sunset
minecraft_hour = (minecraft_time // 1000) % 24
# This gives you the hour (0-23) based on Minecraft time
```

For example:
- Minecraft time 0 = hour 6 (dawn in-game, but hour 6 in our mapping)
- Minecraft time 6000 = hour 12 (noon in-game)
- Minecraft time 12000 = hour 18 (sunset in-game)
- Minecraft time 18000 = hour 0 (midnight in-game)

## Recommendation

**For YouTube banners, real-world time makes more sense** because:
- Viewers see the banner based on their real-world time
- It matches their actual day/night cycle
- More intuitive for your audience

If you want Minecraft-themed banners, you could still name them:
- `00.png` = Midnight (dark/night theme)
- `06.png` = Dawn (sunrise theme)
- `12.png` = Noon (bright/day theme)
- `18.png` = Sunset (evening theme)

But the script will use them based on real-world time, not Minecraft time.

