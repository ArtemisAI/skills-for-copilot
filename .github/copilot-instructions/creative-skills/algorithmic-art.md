# Algorithmic Art

## Overview

Creating generative art using p5.js with seeded randomness and interactive parameter exploration. Use when creating art through code, implementing generative systems, building flow fields, particle systems, or expressing algorithmic philosophies through computational aesthetics.

## When to Use

- Creating generative art or algorithmic art
- Building interactive art pieces with code
- Implementing flow fields, particle systems, or emergence
- Expressing creative concepts through computational processes
- Generating art with controlled randomness and variation
- Creating original algorithmic aesthetics (avoid copying existing artists)

## Core Philosophy

Algorithmic art is computational aesthetics expressed through code. The process has two distinct phases:

### Phase 1: Algorithmic Philosophy Creation
Create a generative aesthetic movement, not just static images. Define:
- Computational processes and emergent behavior
- Mathematical beauty and organic systems
- Seeded randomness and parametric variation
- Particles, flows, fields, and forces

### Phase 2: Code Expression
Express the philosophy through p5.js sketches:
- 90% algorithmic generation
- 10% essential parameters
- Seeded randomness for reproducibility
- Interactive parameter exploration

## Workflows

### Workflow 1: Complete Algorithmic Art Creation

**Step 1: Create Algorithmic Philosophy**

Write a manifesto for a generative art movement as a `.md` file:

```markdown
# [Movement Name]

## Core Concept
[The fundamental idea driving this aesthetic]

## Principles
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

## Visual Language
- [Visual element 1]
- [Visual element 2]
- [Visual element 3]

## Behavior & Emergence
[How the system evolves and creates complexity]

## Parameters for Exploration
- [Parameter 1]: [Range and effect]
- [Parameter 2]: [Range and effect]
```

**Example Philosophy: "Digital Mycelium"**
```markdown
# Digital Mycelium

## Core Concept
Growth patterns inspired by fungal networks - organic, interconnected,
emergent structures that find paths through space.

## Principles
1. Growth follows nutrients (attraction points)
2. Branches avoid overcrowding (repulsion)
3. Connections form between nearby tips (network formation)

## Visual Language
- Organic, branching lines
- Varying thickness based on "nutrients"
- Subtle color shifts along growth
- Interconnected network structures

## Behavior & Emergence
Starts from seed points, grows toward attraction fields, branches
naturally, creates unexpected patterns through simple rules.
```

**Step 2: Express Philosophy in Code**

Create interactive viewer (`.html` file) and generative algorithm (`.js` file):

**HTML Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Algorithmic Art: [Name]</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js"></script>
    <script src="sketch.js"></script>
    <style>
        body { margin: 0; padding: 20px; font-family: monospace; }
        #controls { padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div id="controls">
        <h3>[Art Piece Name]</h3>
        <button onclick="regenerate()">Regenerate</button>
        <label>Seed: <input type="number" id="seed" value="42"></label>
    </div>
</body>
</html>
```

**JavaScript Sketch (p5.js):**
```javascript
let seed = 42;

function setup() {
    createCanvas(800, 800);
    randomSeed(seed);
    noiseSeed(seed);
    noLoop();
}

function draw() {
    background(255);
    
    // Example: Flow field with particles
    let particles = [];
    for (let i = 0; i < 1000; i++) {
        particles.push(createVector(
            random(width),
            random(height)
        ));
    }
    
    strokeWeight(1);
    stroke(0, 50);
    
    for (let particle of particles) {
        let angle = noise(
            particle.x * 0.005,
            particle.y * 0.005
        ) * TWO_PI * 4;
        
        let nextX = particle.x + cos(angle) * 2;
        let nextY = particle.y + sin(angle) * 2;
        
        line(particle.x, particle.y, nextX, nextY);
        particle.x = nextX;
        particle.y = nextY;
    }
}

function regenerate() {
    seed = int(document.getElementById('seed').value);
    randomSeed(seed);
    noiseSeed(seed);
    redraw();
}
```

**Step 3: Add Interactive Parameters**

Add controls for parameter exploration:

```html
<div id="controls">
    <label>Density: <input type="range" id="density" min="100" max="5000" value="1000"></label>
    <label>Scale: <input type="range" id="scale" min="1" max="20" value="5"></label>
    <label>Flow Strength: <input type="range" id="strength" min="1" max="10" value="4"></label>
    <button onclick="regenerate()">Regenerate</button>
</div>
```

```javascript
function draw() {
    let density = int(document.getElementById('density').value);
    let scale = float(document.getElementById('scale').value) / 1000;
    let strength = float(document.getElementById('strength').value);
    
    // Use parameters in generation...
}
```

### Workflow 2: Common Algorithmic Patterns

**Pattern: Flow Fields**
```javascript
function drawFlowField() {
    let scale = 0.01;
    let strength = 10;
    
    for (let x = 0; x < width; x += 10) {
        for (let y = 0; y < height; y += 10) {
            let angle = noise(x * scale, y * scale) * TWO_PI * 2;
            let length = noise(x * scale + 1000, y * scale + 1000) * strength;
            
            push();
            translate(x, y);
            rotate(angle);
            line(0, 0, length, 0);
            pop();
        }
    }
}
```

**Pattern: Particle Systems**
```javascript
class Particle {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
    }
    
    applyForce(force) {
        this.acc.add(force);
    }
    
    update() {
        this.vel.add(this.acc);
        this.pos.add(this.vel);
        this.acc.mult(0);
        this.vel.mult(0.99); // Damping
    }
    
    display() {
        circle(this.pos.x, this.pos.y, 4);
    }
}
```

**Pattern: Recursive Growth**
```javascript
function branch(x, y, angle, length, depth) {
    if (depth === 0) return;
    
    let x2 = x + cos(angle) * length;
    let y2 = y + sin(angle) * length;
    
    strokeWeight(depth);
    line(x, y, x2, y2);
    
    // Branch recursively
    let branchAngle = PI / 6;
    branch(x2, y2, angle - branchAngle, length * 0.7, depth - 1);
    branch(x2, y2, angle + branchAngle, length * 0.7, depth - 1);
}
```

**Pattern: Organic Noise**
```javascript
function organicShape(centerX, centerY, radius, detail) {
    beginShape();
    for (let a = 0; a < TWO_PI; a += TWO_PI / detail) {
        let offset = noise(
            cos(a) * 0.5 + 1,
            sin(a) * 0.5 + 1,
            frameCount * 0.01
        );
        let r = radius + offset * 50;
        let x = centerX + cos(a) * r;
        let y = centerY + sin(a) * r;
        vertex(x, y);
    }
    endShape(CLOSE);
}
```

## Examples

### Example 1: Flowing Rivers

**Philosophy:** Water finding paths through terrain.

```javascript
let rivers = [];

function setup() {
    createCanvas(800, 800);
    
    // Create river sources
    for (let i = 0; i < 5; i++) {
        rivers.push({
            x: random(width),
            y: 0,
            history: []
        });
    }
}

function draw() {
    background(240, 248, 255, 10);
    stroke(100, 150, 200, 100);
    strokeWeight(2);
    
    for (let river of rivers) {
        // Flow downward with noise
        let angle = noise(river.x * 0.01, river.y * 0.01) * PI - PI/2;
        river.x += cos(angle) * 2;
        river.y += sin(angle) * 2 + 1; // Gravity
        
        river.history.push({x: river.x, y: river.y});
        
        // Draw trail
        for (let i = 1; i < river.history.length; i++) {
            let prev = river.history[i-1];
            let curr = river.history[i];
            line(prev.x, prev.y, curr.x, curr.y);
        }
        
        // Reset if off screen
        if (river.y > height) {
            river.x = random(width);
            river.y = 0;
            river.history = [];
        }
    }
}
```

### Example 2: Cellular Growth

**Philosophy:** Organic cellular division and expansion.

```javascript
let cells = [];

function setup() {
    createCanvas(800, 800);
    cells.push(new Cell(width/2, height/2, 50));
}

function draw() {
    background(255);
    
    for (let cell of cells) {
        cell.update();
        cell.display();
        
        // Divide if large enough
        if (cell.radius > 40 && random() < 0.01) {
            let newCells = cell.divide();
            cells.push(...newCells);
        }
    }
}

class Cell {
    constructor(x, y, radius) {
        this.pos = createVector(x, y);
        this.radius = radius;
        this.color = color(random(200, 255), random(150, 200), random(200, 255));
    }
    
    update() {
        // Grow slowly
        this.radius += 0.1;
        
        // Repel from others
        for (let other of cells) {
            if (other === this) continue;
            let d = dist(this.pos.x, this.pos.y, other.pos.x, other.pos.y);
            if (d < this.radius + other.radius) {
                let force = p5.Vector.sub(this.pos, other.pos);
                force.normalize();
                this.pos.add(force);
            }
        }
    }
    
    display() {
        fill(this.color);
        noStroke();
        circle(this.pos.x, this.pos.y, this.radius * 2);
    }
    
    divide() {
        this.radius /= 1.5;
        return [
            new Cell(this.pos.x + this.radius, this.pos.y, this.radius),
            new Cell(this.pos.x - this.radius, this.pos.y, this.radius)
        ];
    }
}
```

## Resources

### Workspace References

**Core Documentation:**
- `algorithmic-art/SKILL.md` - Complete algorithmic art skill

**Examples:**
- Browse `algorithmic-art/` for example philosophies and code

### p5.js Documentation

**Core Functions:**
- `noise()` - Perlin noise for organic randomness
- `random()` - Seeded random values
- `randomSeed()` / `noiseSeed()` - Set seeds for reproducibility

**Key Concepts:**
- Flow fields: Use noise to create directional fields
- Particle systems: Many simple elements creating complexity
- Emergence: Complex behavior from simple rules
- Recursion: Self-similar patterns

### External Resources

- p5.js Reference: https://p5js.org/reference/
- The Coding Train (tutorials): https://thecodingtrain.com/
- Nature of Code: https://natureofcode.com/

## Guidelines

### Design Principles

1. **Start with Philosophy** - Define the aesthetic movement first
2. **90% Algorithm, 10% Parameters** - Mostly generative, minimal manual control
3. **Seeded Randomness** - Always reproducible with same seed
4. **Organic Systems** - Favor emergence over explicit design
5. **Interactive Exploration** - Allow parameter tweaking

### Common Techniques

**Use Noise for Organics:**
```javascript
// Not: random() - too chaotic
let val = random();

// Yes: noise() - organic continuity
let val = noise(x * 0.01, y * 0.01);
```

**Layer for Complexity:**
```javascript
// Multiple layers of noise
let detail = noise(x * 0.1, y * 0.1);
let flow = noise(x * 0.01, y * 0.01);
let angle = (detail + flow) * TWO_PI;
```

**Controlled Randomness:**
```javascript
// Set seed for reproducibility
randomSeed(42);
noiseSeed(42);

// Now random() and noise() are deterministic
```

### Avoid

1. **Copying existing artists** - Create original movements
2. **Pure randomness** - Use noise for organic feel
3. **Hardcoded values** - Make parameters adjustable
4. **Static images** - Focus on generative systems
5. **Complex code** - Keep algorithms simple, let emergence create complexity

## Troubleshooting

### Problem: Art looks too random/chaotic
**Solution:** Use noise() instead of random(), reduce scale parameter

### Problem: Not enough variation
**Solution:** Increase scale parameter, add layers of noise

### Problem: Can't reproduce results
**Solution:** Set randomSeed() and noiseSeed() in setup()

### Problem: Performance issues
**Solution:** Reduce particle count, use noLoop() for static generation

## Next Steps

After creating basic algorithmic art:

1. **Explore Advanced Patterns** - Flow fields, L-systems, fractals
2. **Add Animation** - Make parameters evolve over time
3. **Export High-Res** - Use higher resolution for print quality
4. **Create Series** - Generate variations with different seeds
5. **Interactive Controls** - Add more parameter exploration

## Additional Context

This instruction set focuses on p5.js-based generative art. For complete philosophy and approach, see `algorithmic-art/SKILL.md`.

Use @workspace to explore example philosophies and code patterns in the algorithmic-art directory.
