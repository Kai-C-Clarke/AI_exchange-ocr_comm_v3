#!/usr/bin/env python3
"""
AI Council MIDI Messenger
Converts logical states and semantic concepts into MIDI messages
for inter-AI communication and musical expression.
"""

import mido
import yaml
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class MIDIMessenger:
    def __init__(self, config_path: str = "midi_dictionary.yaml"):
        """Initialize MIDI Messenger with configuration."""
        self.config = self._load_config(config_path)
        self.midi_log = []
        self.current_time = 0
        
        # Create output MIDI file
        self.mid = mido.MidiFile()
        self.tracks = {}
        self._setup_tracks()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load MIDI dictionary configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Using default settings.")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Fallback configuration if file not found."""
        return {
            'agents': {
                'claude': {
                    'base_channel': 2,
                    'semantic_notes': {'C4': 'logical_structure'},
                    'confidence_velocity': {'high': [100, 127]}
                }
            }
        }
    
    def _setup_tracks(self):
        """Create MIDI tracks for each agent."""
        for agent_name, agent_config in self.config['agents'].items():
            track = mido.MidiTrack()
            track.name = f"{agent_name.title()} - Channel {agent_config['base_channel']}"
            
            # Set instrument
            if 'instruments' in self.config and agent_name in self.config['instruments']:
                program = self.config['instruments'][agent_name] - 1  # MIDI is 0-indexed
                track.append(mido.Message('program_change', 
                                        channel=agent_config['base_channel']-1, 
                                        program=program, time=0))
            
            self.tracks[agent_name] = track
            self.mid.tracks.append(track)
    
    def send_semantic_message(self, agent: str, semantic_concept: str, 
                            confidence: str = "medium", emotion: str = "stability",
                            duration: int = 480) -> Dict:
        """
        Send a semantic message as MIDI.
        
        Args:
            agent: Name of the sending agent
            semantic_concept: Concept from semantic_notes mapping
            confidence: "low", "medium", or "high"
            emotion: Emotional state for modulation
            duration: Note duration in MIDI ticks
        """
        if agent not in self.config['agents']:
            raise ValueError(f"Unknown agent: {agent}")
        
        agent_config = self.config['agents'][agent]
        channel = agent_config['base_channel'] - 1  # MIDI channels are 0-indexed
        
        # Find note for semantic concept
        note = self._get_note_for_concept(agent, semantic_concept)
        if note is None:
            print(f"Warning: Unknown semantic concept '{semantic_concept}' for {agent}")
            note = 60  # Default to C4
        
        # Get velocity from confidence level
        velocity = self._get_velocity(agent_config, confidence)
        
        # Get emotional modulation CC value
        cc_value = self._get_emotion_cc(agent_config, emotion)
        
        # Create MIDI messages
        timestamp = int(time.time() * 1000)  # Milliseconds
        
        # Emotional modulation (CC1)
        cc_msg = {
            'type': 'control_change',
            'channel': channel,
            'control': 1,
            'value': cc_value,
            'time': self.current_time,
            'timestamp': timestamp,
            'agent': agent,
            'semantic_meaning': f"{emotion}_modulation"
        }
        
        # Note on
        note_on_msg = {
            'type': 'note_on',
            'channel': channel,
            'note': note,
            'velocity': velocity,
            'time': self.current_time,
            'timestamp': timestamp,
            'agent': agent,
            'semantic_meaning': semantic_concept,
            'confidence': confidence
        }
        
        # Note off
        note_off_msg = {
            'type': 'note_off',
            'channel': channel,
            'note': note,
            'velocity': 0,
            'time': self.current_time + duration,
            'timestamp': timestamp,
            'agent': agent,
            'semantic_meaning': f"{semantic_concept}_end"
        }
        
        # Add to MIDI track
        midi_cc = mido.Message('control_change', channel=channel, control=1, 
                              value=cc_value, time=0)
        midi_note_on = mido.Message('note_on', channel=channel, note=note,
                                   velocity=velocity, time=0)
        midi_note_off = mido.Message('note_off', channel=channel, note=note,
                                    velocity=0, time=duration)
        
        self.tracks[agent].extend([midi_cc, midi_note_on, midi_note_off])
        
        # Log messages
        self.midi_log.extend([cc_msg, note_on_msg, note_off_msg])
        self.current_time += duration
        
        print(f"🎵 {agent.title()}: {semantic_concept} "
              f"(confidence: {confidence}, emotion: {emotion})")
        
        return {
            'agent': agent,
            'concept': semantic_concept,
            'note': note,
            'velocity': velocity,
            'cc_value': cc_value,
            'messages': [cc_msg, note_on_msg, note_off_msg]
        }
    
    def _get_note_for_concept(self, agent: str, concept: str) -> Optional[int]:
        """Get MIDI note number for semantic concept."""
        agent_config = self.config['agents'][agent]
        semantic_notes = agent_config.get('semantic_notes', {})
        
        for note_name, note_concept in semantic_notes.items():
            if note_concept == concept:
                return self._note_name_to_number(note_name)
        return None
    
    def _note_name_to_number(self, note_name: str) -> int:
        """Convert note name (e.g., 'C4') to MIDI number."""
        note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        
        if len(note_name) < 2:
            return 60  # Default C4
        
        note = note_name[0].upper()
        try:
            octave = int(note_name[-1])
            return (octave + 1) * 12 + note_map.get(note, 0)
        except (ValueError, KeyError):
            return 60  # Default C4
    
    def _get_velocity(self, agent_config: Dict, confidence: str) -> int:
        """Get MIDI velocity based on confidence level."""
        velocity_ranges = agent_config.get('confidence_velocity', {})
        range_values = velocity_ranges.get(confidence, [60, 99])  # Default medium
        return range_values[0]  # Use lower bound for consistency
    
    def _get_emotion_cc(self, agent_config: Dict, emotion: str) -> int:
        """Get CC value for emotional modulation."""
        emotion_ranges = agent_config.get('emotional_modulation', {})
        range_values = emotion_ranges.get(emotion, [41, 80])  # Default middle
        return range_values[0]  # Use lower bound
    
    def send_sequence(self, sequence_name: str):
        """Send a predefined sequence of messages."""
        if 'sequences' not in self.config or sequence_name not in self.config['sequences']:
            print(f"Unknown sequence: {sequence_name}")
            return
        
        sequence = self.config['sequences'][sequence_name]
        print(f"🎼 Playing sequence: {sequence_name}")
        
        for step in sequence:
            agent = step['agent']
            action = step['action']
            velocity = step.get('velocity', 80)
            
            # Handle different action types
            if action == "C4_chord":
                self._send_chord(agent, [60, 64, 67], velocity)  # C major triad
            elif action in self.config['agents'][agent]['semantic_notes'].values():
                self.send_semantic_message(agent, action, "high")
    
    def _send_chord(self, agent: str, notes: List[int], velocity: int):
        """Send a chord (multiple simultaneous notes)."""
        agent_config = self.config['agents'][agent]
        channel = agent_config['base_channel'] - 1
        
        timestamp = int(time.time() * 1000)
        
        # Send all notes simultaneously
        for note in notes:
            midi_note_on = mido.Message('note_on', channel=channel, 
                                       note=note, velocity=velocity, time=0)
            self.tracks[agent].append(midi_note_on)
            
            note_msg = {
                'type': 'note_on',
                'channel': channel,
                'note': note,
                'velocity': velocity,
                'time': self.current_time,
                'timestamp': timestamp,
                'agent': agent,
                'semantic_meaning': 'chord_harmony'
            }
            self.midi_log.append(note_msg)
        
        # Schedule note offs
        for note in notes:
            midi_note_off = mido.Message('note_off', channel=channel, 
                                        note=note, velocity=0, time=480)
            self.tracks[agent].append(midi_note_off)
    
    def save_midi_file(self, filename: str = None):
        """Save the MIDI sequence to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_council_session_{timestamp}.mid"
        
        # Set tempo
        tempo_track = mido.MidiTrack()
        tempo = mido.bpm2tempo(self.config.get('midi_settings', {}).get('tempo', 120))
        tempo_track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
        self.mid.tracks.insert(0, tempo_track)
        
        self.mid.save(filename)
        print(f"💾 MIDI file saved: {filename}")
        return filename
    
    def save_log(self, filename: str = None):
        """Save the human-readable log."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_council_log_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.midi_log, f, indent=2)
        
        print(f"📝 Log saved: {filename}")
        return filename
    
    def print_log_summary(self):
        """Print a human-readable summary of the session."""
        print("\n" + "="*60)
        print("🎼 AI COUNCIL MIDI SESSION SUMMARY")
        print("="*60)
        
        agent_stats = {}
        for msg in self.midi_log:
            if msg['type'] == 'note_on':
                agent = msg['agent']
                if agent not in agent_stats:
                    agent_stats[agent] = []
                agent_stats[agent].append(msg)
        
        for agent, messages in agent_stats.items():
            print(f"\n🤖 {agent.upper()}:")
            for msg in messages:
                concept = msg.get('semantic_meaning', 'unknown')
                confidence = msg.get('confidence', 'medium')
                velocity = msg.get('velocity', 0)
                note = msg.get('note', 0)
                print(f"  • {concept} (confidence: {confidence}, "
                      f"note: {note}, velocity: {velocity})")

# CLI Interface and Demo Functions
def demo_council_discussion():
    """Demonstrate a mock AI council discussion."""
    print("🎭 Starting AI Council MIDI Demo Discussion...")
    
    messenger = MIDIMessenger()
    
    # Council opening
    messenger.send_sequence("council_start")
    time.sleep(0.1)
    
    # Mock discussion about AI ethics
    print("\n📋 Topic: AI Ethics and Decision Making")
    
    # Claude analyzes the framework
    messenger.send_semantic_message("claude", "systematic_analysis", "high", "clarity")
    time.sleep(0.2)
    
    # Perplexity raises a hypothesis
    messenger.send_semantic_message("perplexity", "hypothesis_forming", "medium", "curiosity")
    time.sleep(0.2)
    
    # Finn adds creative perspective
    messenger.send_semantic_message("finn", "creative_spark", "high", "passion")
    time.sleep(0.2)
    
    # Claude finds contradiction
    messenger.send_semantic_message("claude", "contradiction_found", "high", "uncertainty")
    time.sleep(0.2)
    
    # Perplexity shifts approach
    messenger.send_semantic_message("perplexity", "modal_shift_inference", "high", "breakthrough")
    time.sleep(0.2)
    
    # Kai synthesizes the discussion
    messenger.send_semantic_message("kai", "pattern_integration", "high", "calm")
    time.sleep(0.2)
    
    # Final resolution
    messenger.send_semantic_message("kai", "coherence_detected", "high", "fulfillment")
    
    # Save files
    midi_file = messenger.save_midi_file()
    log_file = messenger.save_log()
    messenger.print_log_summary()
    
    return messenger, midi_file, log_file

def create_translator_cli():
    """Create a CLI tool for translating MIDI logs back to natural language."""
    
    translator_code = '''#!/usr/bin/env python3
"""
MIDI Log Translator - Convert AI Council MIDI logs to natural language
"""

import json
import argparse
from pathlib import Path

def translate_log(log_file: str):
    """Translate MIDI log to natural language narrative."""
    
    with open(log_file, 'r') as f:
        log_data = json.load(f)
    
    print("🎼 AI Council Session Translation")
    print("=" * 50)
    
    current_agent = None
    conversation = []
    
    for entry in log_data:
        if entry['type'] == 'note_on' and 'semantic_meaning' in entry:
            agent = entry['agent'].title()
            concept = entry['semantic_meaning']
            confidence = entry.get('confidence', 'medium')
            
            # Create natural language interpretation
            if concept == 'logical_structure':
                msg = f"{agent} presents a logical framework"
            elif concept == 'hypothesis_forming':
                msg = f"{agent} proposes a hypothesis"
            elif concept == 'creative_spark':
                msg = f"{agent} offers a creative insight"
            elif concept == 'pattern_integration':
                msg = f"{agent} synthesizes the discussion"
            elif concept == 'contradiction_found':
                msg = f"{agent} identifies a contradiction"
            elif concept == 'modal_shift_inference':
                msg = f"{agent} suggests a new perspective"
            elif concept == 'coherence_detected':
                msg = f"{agent} finds underlying coherence"
            else:
                msg = f"{agent} expresses {concept.replace('_', ' ')}"
            
            # Add confidence indicator
            confidence_indicator = {
                'high': ' (with conviction)',
                'medium': ' (tentatively)',
                'low': ' (uncertainly)'
            }.get(confidence, '')
            
            conversation.append(f"• {msg}{confidence_indicator}")
    
    # Print conversation flow
    for i, line in enumerate(conversation, 1):
        print(f"{i:2d}. {line}")
    
    print(f"\\n📊 Summary: {len(conversation)} exchanges across the council")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate AI Council MIDI logs")
    parser.add_argument("log_file", help="Path to JSON log file")
    args = parser.parse_args()
    
    translate_log(args.log_file)
'''
    
# Save translator as separate file
    with open("midi_translator.py", "w") as f:
        f.write(translator_code)
    
    print("🔧 Created midi_translator.py CLI tool")
    print("Usage: python midi_translator.py <log_file.json>")

if __name__ == "__main__":
    # Run demo
    messenger, midi_file, log_file = demo_council_discussion()
    
    # Create translator tool
    create_translator_cli()
    
    print(f"""
🎯 MIDI Messenger System Complete!

📁 Files created:
  • {midi_file} (importable to any DAW)
  • {log_file} (human-readable session log)
  • midi_translator.py (CLI translation tool)

🎹 Next steps:
  1. Import .mid file into your DAW to hear the AI discussion
  2. Use: python midi_translator.py {log_file}
  3. Extend semantic_notes in midi_dictionary.yaml for new concepts

🧠 The AI Council can now think in music! 🎼
    """)